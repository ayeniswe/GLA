from plugins.resolver.resolver import BestResolver, Resolver
from utilities.strategy import RegexStrategy, ScoringStrategy
from re import compile


def test_resolver():
    resolve = Resolver(
        [
            RegexStrategy(compile(r"(\d{4}-\d{2}-\d{2})")),
            RegexStrategy(compile(r"(\d)")),
        ],
        False,
    )

    assert resolve.resolve("2024-04-01") is not None
    assert resolve.resolve("43434434") is not None
    assert resolve.resolve(" ") is None


def test_resolver_cache():
    resolve = Resolver(
        [
            RegexStrategy(compile(r"(\d{4}-\d{2}-\d{2})")),
            RegexStrategy(compile(r"(\d)")),
        ],
        True,
    )

    assert resolve.resolve("2024-04-01") is not None
    assert resolve.resolve("434243") is None
    assert resolve.resolve(" ") is None


def test_best_resolver():
    class CustomStrategy(ScoringStrategy):
        def __init__(self, text: str):
            self._text = text

        def score(self, entry: str):
            return (abs(len(entry) - len(self._text)), self._text)

    resolve = BestResolver(
        [
            CustomStrategy("hello"),
            CustomStrategy("hello_world"),
        ],
        False,
    )

    assert resolve.resolve("test") == "hello_world"
    assert resolve.resolve("longgggggggggg") == "hello"


def test_best_resolver_cache():
    class CustomStrategy(ScoringStrategy):
        def __init__(self, text: str):
            self._text = text

        def score(self, entry: str):
            return (abs(len(entry) - len(self._text)), self._text)

    resolve = BestResolver(
        [
            CustomStrategy("hello"),
            CustomStrategy("hello_world"),
        ],
        True,
    )

    assert resolve.resolve("test") == "hello_world"
    assert resolve.resolve("longgggggggggg") == "hello_world"
    assert resolve.resolve("verylonggggg") == "hello_world"
