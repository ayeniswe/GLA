"""
The 'json_transformer' module defines the `JsonTransformer` class, which is responsible
for transforming JSON log messages into structured `Log` objects based on predefined
schema mappings.
"""

from json import JSONDecodeError, loads
from typing import Any, Dict, Optional, Tuple

import dateparser

from gla.analyzer.iterator import Mode, Structured, StructuredMixIn, UnstructuredBaseResolverBreakerMixIn
from gla.constants import LANGUAGES_SUPPORTED
from gla.models.log import Log
from gla.plugins.resolver.resolver import BestResolver
from gla.plugins.transformer.transformer import BaseTransformerValidator, Breaker
from gla.typings.alias import FileDescriptorOrPath
from gla.utilities.strategy import  ScoringStrategyAction


class JsonStrategy(ScoringStrategyAction):
    """
    The `JsonStrategy` class is responsible for handling strategies based on json key mappings
    """

    def __init__(self, mapping: dict):
        self._mapping = mapping

    def score(self, entry: Tuple[FileDescriptorOrPath, str]) -> Tuple[int, dict]:
        for line in Structured(entry[0], entry[1], Mode.JSON):
            return (
                sum(1 for field in self._mapping.values() if field in line),
                self._mapping,
            )
    
    def do_action(self, _: dict):
        return self._mapping


class JsonTransformer(BaseTransformerValidator, BestResolver, StructuredMixIn):
    """
    The `JsonTransformer` class is responsible for handling transformation
    of `json` log messages
    """
    
    @property
    def mode(self) -> str:
        return Mode.JSON

    def __init__(self, cache: bool = False):
        """Create a new `JsonTransformer`

        NOTE: cache set to `True` will enable the use of the same strategy for
        future log entries seen by this instance
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
            cache,
        )

    def transform(self, entry: str) -> Optional[Log]:
        try:
            res: dict = loads(entry.strip())
            mapping: dict = self._cache_strategy.do_action()
            if mapping:
                time = res.get(mapping.get("timestamp"))
                if time is not None:
                    time = dateparser.parse(time, languages=LANGUAGES_SUPPORTED)
                return Log(
                    level=res.get(mapping.get("level")),
                    module=res.get(mapping.get("module")),
                    source=res.get(mapping.get("source")),
                    timestamp=time,
                    message=res.get(
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
