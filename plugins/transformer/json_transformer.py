from json import JSONDecodeError, loads
from os import PathLike
import dateparser
from typing import Optional, Tuple
from models.log import Log
from plugins.resolver.resolver import BestResolver
from plugins.transformer.transformer import BaseTransformer
from typeguard import typechecked
from utilities.strategy import ScoringStrategy


@typechecked
class JsonStrategy(ScoringStrategy):
    """
    The `JsonStrategy` class is responsible for handling strategies based on json key mappings
    """

    def __init__(self, mapping: dict):
        self._mapping = mapping

    def score(self, entry: dict) -> Tuple[int, dict]:
        return (
            sum(1 for field in self._mapping.values() if field in entry),
            self._mapping,
        )


@typechecked
class JsonTransformer(BaseTransformer, BestResolver):
    """
    The `JsonTransformer` class is responsible for handling transformation
    of `json` log messages
    """

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

    def _transform(self, line: str) -> Optional[Log]:
        try:
            res: dict = loads(line.strip())
            mapping: Optional[dict] = self.resolve(res)
            return Log(
                level=res.get(mapping.get("level")),
                module=res.get(mapping.get("module")),
                source=res.get(mapping.get("source")),
                timestamp=dateparser.parse(res.get(mapping.get("timestamp"))),
                message=res.get(
                    mapping.get("message"),
                ),
            )
        except JSONDecodeError:
            return None

    def _validate(self, path: PathLike) -> bool:
        with open(path, "r") as file:
            try:
                return loads(file.readline().strip()) is not None
            except JSONDecodeError:
                return False
