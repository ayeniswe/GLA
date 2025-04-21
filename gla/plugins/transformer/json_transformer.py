"""
The 'json_transformer' module defines the `JsonTransformer` class, which is responsible
for transforming JSON log messages into structured `Log` objects based on predefined
schema mappings.
"""

from json import JSONDecodeError
from typing import Any, Dict, Optional, Tuple

import dateparser

from gla.analyzer.iterator import Mode, Structured, StructuredMixIn
from gla.constants import LANGUAGES_SUPPORTED
from gla.models.log import Log
from gla.plugins.resolver.resolver import BestResolver
from gla.plugins.transformer.transformer import BaseTransformerValidator
from gla.typings.alias import FileDescriptorOrPath
from gla.utilities.strategy import  ScoringStrategyArtifact


class JsonStrategy(ScoringStrategyArtifact):
    """
    The `JsonStrategy` class is responsible for handling strategies based on json key mappings
    """

    def __init__(self, mapping: dict):
        self._mapping = mapping

    def score(self, entry: Tuple[FileDescriptorOrPath, str]) -> Tuple[int, dict]:
        for line in Structured(entry[0], entry[1], Mode.JSON):
            line_keys: set = set(line.keys())
            mapping_values: set = set(self._mapping.values())
            
            # Overlap Coefficient Similiarity Heuristic
            intersect = len(line_keys.intersection(mapping_values)) 
            min_size = min(len(mapping_values), len(line_keys)) 
            return intersect / min_size
    
    def artifact(self):
        return self._mapping


class JsonTransformer(BaseTransformerValidator, BestResolver, StructuredMixIn):
    """
    The `JsonTransformer` class is responsible for handling transformation
    of `json` log messages
    """
    
    @property
    def mode(self) -> str:
        return Mode.JSON

    def __init__(self):
        """Create a new `JsonTransformer`
        """
        super().__init__(
            [
                # Elastic Common Schema
                JsonStrategy(
                    {
                        "level": "log.level",
                        "module": "log.logger",
                        "source": "service.name",
                        "timestamp": "@timestamp",
                        "message": "message",
                    }
                ),
                # Log4j Schema
                JsonStrategy(
                    {
                        "level": "level",
                        "module": "loggerName",
                        "source": "threadName",
                        "timestamp": "timestamp",
                        "message": "message",
                    }
                ),
                # Syslog Schema
                JsonStrategy(
                    {
                        "level": "severity",
                        "module": "appname",
                        "source": "host",
                        "timestamp": "timestamp",
                        "message": "msg",
                    }
                ),
            ],
            False
        )

    def transform(self, entry: dict) -> Optional[Log]:
        try:
            mapping: dict = self._cache_strategy.artifact()
            if mapping:
                time = entry.get(mapping.get("timestamp"))
                if time is not None:
                    time = dateparser.parse(time, languages=LANGUAGES_SUPPORTED)
                return Log(
                    level=entry.get(mapping.get("level")),
                    module=entry.get(mapping.get("module")),
                    source=entry.get(mapping.get("source")),
                    timestamp=time,
                    message=entry.get(
                        mapping.get("message"),
                    ),
                )
            return None
        except JSONDecodeError:
            return None

    def validate(self, data: Dict[str, Any]) -> bool:
        try:
           return self.resolve((data["data"], data["encoding"])) is not None
        except (FileNotFoundError, UnicodeDecodeError, JSONDecodeError):
            return False
