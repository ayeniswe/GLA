import os
import pytest

@pytest.fixture
def get_log_path():
    def _inner(filename: str) -> str:
        return os.path.join(os.path.dirname(__file__), "logs", filename)
    return _inner
