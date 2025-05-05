from re import compile

from gla.plugins.resolver.resolver import BestResolver, Resolver
from gla.utilities.strategy import RegexStrategy, ScoringStrategy


def test_resolver():
    # ARRANGE
    strat1 = RegexStrategy(compile(r"(\d{4}-\d{2}-\d{2})"))
    strat2 = RegexStrategy(compile(r"(\d)"))
    resolve = Resolver(
        [strat1, strat2],
        False,
    )

    # ACT
    res = resolve.resolve("2024-04-01")
    res2 = resolve.resolve("434243")
    res3 = resolve.resolve(" ")

    # ASSERT
    assert res == strat1
    assert res2 == strat2
    assert res3 is None


def test_resolver_cache():
    # ARRANGE
    strat1 = RegexStrategy(compile(r"(\d{4}-\d{2}-\d{2})"))
    strat2 = RegexStrategy(compile(r"(\d)"))
    resolve = Resolver(
        [strat1, strat2],
        True,
    )

    # ACT
    res = resolve.resolve("2024-04-01")
    res2 = resolve.resolve("434243")
    res3 = resolve.resolve(" ")

    # ASSERT
    assert res == strat1
    assert res2 == strat1
    assert res3 == strat1


def test_best_resolver():
    # ARRANGE
    class CustomStrategy(ScoringStrategy):
        def __init__(self, text: str):
            self._text = text

        def score(self, entry: str):
            return abs(len(entry) - len(self._text))

    strat1 = CustomStrategy("hello")
    strat2 = CustomStrategy("hello_world")
    resolve = BestResolver(
        [
            strat1,
            strat2,
        ],
        False,
    )

    # ACT
    res = resolve.resolve("test")
    res2 = resolve.resolve("longgggggggggg")

    # ASSERT
    assert res == strat2
    assert res2 == strat1


def test_best_resolver_cache():
    # ARRANGE
    class CustomStrategy(ScoringStrategy):
        def __init__(self, text: str):
            self._text = text

        def score(self, entry: str):
            return abs(len(entry) - len(self._text))

    strat1 = CustomStrategy("hello")
    strat2 = CustomStrategy("hello_world")
    resolve = BestResolver(
        [
            strat1,
            strat2,
        ],
        True,
    )

    # ACT
    res = resolve.resolve("test")
    res2 = resolve.resolve("longgggggggggg")
    res3 = resolve.resolve("verylonggggg")

    # ASSERT
    assert res == strat2
    assert res2 == strat2
    assert res3 == strat2
