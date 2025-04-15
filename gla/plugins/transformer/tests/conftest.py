import os
from typing import Any, Dict, Iterator

import pytest

from gla.plugins.transformer.transformer import BaseTransformer


@pytest.fixture
def get_log_path():
    def _inner(filename: str) -> str:
        return os.path.join(os.path.dirname(__file__), "logs", filename)
    return _inner

@pytest.fixture
def check_transformer_test_cases():
    def _inner(cases: Dict[str, Any], iterator: Iterator, trans: BaseTransformer) -> str:
        for idx, entry in enumerate(iterator):
            # ACT
            result = trans.transform(entry)
            result = str(result) if result else result

            # ASSERT
            try:
                actual = cases[idx]["expected"]
            except KeyError:
                raise KeyError("Every expected case must have a single key named 'expected'")
            except IndexError:
                raise IndexError("An expected case must be specified for each iteration of tests")
            assert (result == actual)
    return _inner
