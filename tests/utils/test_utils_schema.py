from pathlib import Path
from plone.distribution.utils import schema as utils_schema

import json
import pytest


@pytest.fixture
def data_path() -> Path:
    cur_dir = Path(__file__).parent.resolve()
    return cur_dir / "data"


@pytest.fixture
def valid_schema(data_path):
    return json.loads((data_path / "valid.json").read_text())


@pytest.fixture
def invalid_schema(data_path):
    return json.loads((data_path / "invalid.json").read_text())


class TestUtilsSchemaValidateJsonSchema:
    @property
    def func(self):
        return utils_schema.validate_jsonschema

    def test_validate_jsonschema_success(self, app, valid_schema):
        schema = valid_schema["schema"]
        result = self.func(schema)
        assert result is True

    def test_validate_jsonschema_fail(self, app, invalid_schema):
        schema = invalid_schema["schema"]
        result = self.func(schema)
        assert result is False

    def test_validate_jsonschema_strict_fail(self, app, valid_schema):
        schema = valid_schema["schema"]
        # Remove default_language property (that is only recommended, not required)
        del schema["properties"]["default_language"]
        result = self.func(schema, strict=True)
        assert result is False


class TestUtilsSchemaEnrichJsonSchema:
    @property
    def func(self):
        return utils_schema.enrich_jsonschema

    @pytest.mark.parametrize("key", ["languages", "timezones"])
    def test_enrich_jsonschema(self, app, key):
        schema = {}
        result = self.func(schema)
        assert "definitions" in result
        definitions = result["definitions"]
        assert key in definitions


class TestUtilsSchemaEnrichUiSchema:
    @property
    def func(self):
        return utils_schema.enrich_uischema

    def test_enrich_uischema(self, app, valid_schema):
        jsonschema = valid_schema["schema"]
        uischema = valid_schema["uischema"]
        assert len(uischema) == 0
        result = self.func(uischema, jsonschema)
        assert result["ui:order"][0] == "site_id"
        assert result["ui:order"][1] == "title"
        assert result["ui:order"][2] == "description"


class TestUtilsSchemaProcessRawSchema:
    @property
    def func(self):
        return utils_schema.process_raw_schema

    def test_enrich_uischema(self, app, valid_schema):
        result = self.func(valid_schema)
        assert "schema" in result
        assert "uischema" in result
        uischema = result["uischema"]
        assert "ui:order" in uischema
