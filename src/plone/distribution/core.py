from datetime import datetime
from pathlib import Path
from Persistence import Persistent
from plone.distribution import BASE_DISTRIBUTIONS_PATH
from plone.distribution.utils import schema as schema_utils
from typing import Callable
from typing import List

import json


DEFAULT_SCHEMA = json.load(open(BASE_DISTRIBUTIONS_PATH / "default" / "schema.json"))
DEFAULT_IMAGE = BASE_DISTRIBUTIONS_PATH / "default" / "image.png"


class Distribution:
    name: str
    title: str
    description: str
    directory: Path
    handler: Callable
    post_handler: Callable
    _schema: dict
    _profiles: dict

    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        directory: Path,
        handler: Callable = None,
        post_handler: Callable = None,
    ):
        """Initialize a Plone Distribution."""
        self.name = name
        self.title = title
        self.description = description
        self.directory = directory
        self.handler = handler
        self.post_handler = post_handler
        schema_file = self.directory / "schema.json"
        raw_schema = DEFAULT_SCHEMA
        if schema_file.exists():
            try:
                raw_schema = json.loads(schema_file.read_text())
            except json.JSONDecodeError:
                # Log error
                pass
        schema = schema_utils.process_raw_schema(raw_schema)
        if not schema_utils.validate_jsonschema(schema["schema"]):
            raise ValueError(f"Invalid schema for {schema_file}")
        self._schema = schema
        profiles = {"base": [], "content": []}
        data_file = self.directory / "profiles.json"
        if data_file.exists():
            profiles = json.load(open(data_file))
        self._profiles = profiles

    def __repr__(self) -> str:
        return f"<Distribution name='{self.name}' title='{self.title}'>"

    @property
    def image(self) -> Path:
        """Return path to distribution image."""
        image = self.directory / "image.png"
        return image if image.exists() else DEFAULT_IMAGE

    @property
    def _content_folder(self) -> Path:
        """Return folder to example content."""
        folder = self.directory / "content"
        return folder

    @property
    def schema(self) -> dict:
        """Return a valid JSONSchema."""
        # We have to run enrich_jsonschema here because languages and
        # timezones may not be available during startup
        return schema_utils.enrich_jsonschema(self._schema["schema"])

    @property
    def uischema(self) -> dict:
        """Return the ui schema."""
        return self._schema["uischema"]

    @property
    def profiles(self) -> List[str]:
        """Return a list of profiles to be applied."""
        main_profiles = self._profiles.get("base", [])
        return main_profiles

    @property
    def contents(self) -> dict:
        """Return content structure."""
        content_folder = self._content_folder
        content_profiles = self._profiles.get("content", [])
        return {
            "profiles": content_profiles,
            "json": content_folder if content_folder.exists() else None,
        }


class SiteCreationReport(Persistent):
    name: str
    date: datetime
    _answers: str

    def __init__(self, name: str, date: datetime, answers: dict):
        """Initialize the report."""
        self.name = name
        self.date = date
        self._answers = tuple([(k, v) for k, v in answers.items()])

    @property
    def answers(self) -> dict:
        """Return original answers."""
        return dict(self._answers)
