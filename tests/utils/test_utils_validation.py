from plone.distribution.utils import schema as utils_schema
from plone.distribution.utils import validation

import pytest


@pytest.fixture
def schema(valid_schema) -> dict:
    return utils_schema.enrich_jsonschema(valid_schema["schema"])


@pytest.fixture
def valid_answers() -> dict:
    return {
        "site_id": "Plone",
        "title": "Testing Plone Site",
        "description": "A new Plone Site",
        "default_language": "en",
        "portal_timezone": "UTC",
        "setup_content": True,
    }


@pytest.fixture
def invalid_answers() -> dict:
    return {
        "site_id": "Plone",
        "title": 123,
        "description": "A new Plone Site",
        "default_language": "en",
        "portal_timezone": "UTC",
        "setup_content": True,
    }


class TestUtilsSchemaValidateAnswers:
    @pytest.fixture(autouse=True)
    def _init(self, app):
        self.app = app

    @property
    def func(self):
        return validation.validate_answers

    def test_valid_schema_valid_answers(self, valid_answers, schema):
        result = self.func(valid_answers, schema)
        assert result is True

    def test_valid_schema_invalid_answers(self, invalid_answers, schema):
        result = self.func(invalid_answers, schema)
        assert result is False

    def test_invalid_schema_valid_answers(self, valid_answers, invalid_schema):
        schema = invalid_schema["schema"]
        result = self.func(valid_answers, schema)
        assert result is False

    def test_invalid_schema_invalid_answers(self, invalid_answers, invalid_schema):
        schema = invalid_schema["schema"]
        result = self.func(invalid_answers, schema)
        assert result is False
