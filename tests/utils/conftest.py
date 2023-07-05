from pathlib import Path

import json
import pytest


@pytest.fixture
def data_path() -> Path:
    cur_dir = Path(__file__).parent.resolve()
    return cur_dir / "data"


@pytest.fixture
def language_schema(data_path):
    return json.loads((data_path / "with_default_language.json").read_text())


@pytest.fixture
def valid_schema(data_path):
    return json.loads((data_path / "valid.json").read_text())


@pytest.fixture
def invalid_schema(data_path):
    return json.loads((data_path / "invalid.json").read_text())
