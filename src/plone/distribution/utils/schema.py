from plone.i18n.locales.interfaces import IContentLanguageAvailability
from zope.component import getGlobalSiteManager
from zope.component import getUtility
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory


def _common_timezones():
    """Return a list of common timezones to be used during site creation."""
    context = getGlobalSiteManager()
    tz_vocab = getUtility(IVocabularyFactory, "plone.app.vocabularies.CommonTimezones")(
        context
    )

    response = []
    for term in tz_vocab:
        value = term.value
        split_value = value.split("/")
        friendly = split_value[-1]
        label = f"{friendly} ({value})"
        response.append({"label": label, "value": value})

    return response


def _available_languages() -> list:
    """Return available languages."""
    util = queryUtility(IContentLanguageAvailability)
    available = util.getLanguages(combined=True)
    languages = dict(util.getLanguageListing())

    # Group country specific versions by language
    grouped = {}
    for langcode, data in available.items():
        lang = langcode.split("-")[0]
        language = languages.get(lang, lang)  # Label

        struct = grouped.get(lang, {"label": language, "languages": []})

        langs = struct["languages"]
        langs.append(
            {
                "langcode": langcode,
                "label": data.get("native", data.get("name")),
            }
        )

        grouped[lang] = struct

    # Sort list by language, next by country
    response = []
    data = sorted(grouped.values(), key=lambda k: k["label"])
    for item in data:
        langs = sorted(item["languages"], key=lambda k: k["label"].lower())
        response.extend(langs)
    return response


def enrich_jsonschema(schema: dict) -> dict:
    """Process a jsonschema, adding definitions."""
    if "definitions" not in schema:
        schema["definitions"] = {}
    # Only add languages if does not exists
    if "languages" not in schema["definitions"]:
        languages = _available_languages()
        schema["definitions"]["languages"] = {
            "title": "Language",
            "type": "string",
            "default": "en",
            "description": "The main language of the site.",
            "anyOf": [
                {
                    "type": "string",
                    "enum": [lang["langcode"]],
                    "title": lang["label"],
                }
                for lang in languages
            ],
        }
    # Only add timezones if does not exists
    if "timezones" not in schema["definitions"]:
        # Set timezones
        schema["definitions"]["timezones"] = {
            "title": "Timezone",
            "type": "string",
            "default": "UTC",
            "description": (
                "The default timezone setting of the portal. "
                "Users will be able to set their own timezone, "
                "if available timezones are defined in the date "
                "and time settings."
            ),
            "anyOf": [
                {"type": "string", "enum": [tz["value"]], "title": tz["label"]}
                for tz in _common_timezones()
            ],
        }
    return schema


def enrich_uischema(uischema: dict, jsonschema: dict) -> dict:
    """Process a uischema and set default ordering (if not present)."""
    if "ui:order" not in uischema:
        # Set order to be the same as defined in the original schema creation.
        properties = [k for k in jsonschema["properties"].keys()]
        uischema["ui:order"] = properties
    return uischema


def process_raw_schema(raw_schema: dict) -> dict:
    """Process a schema file adding definitions and setting a default uischema."""
    jsonschema = raw_schema["schema"]
    uischema = enrich_uischema(raw_schema.get("uischema", {}), jsonschema)
    return {"schema": jsonschema, "uischema": uischema}


def validate_jsonschema(schema: dict, strict: bool = False) -> bool:
    """Validate if jsonschema has required information."""
    required_properties = ["site_id", "title", "setup_content"]
    if strict:
        required_properties.extend(["default_language", "portal_timezone"])
    properties = [key for key in schema.get("properties")]
    missing = [key for key in required_properties if key not in properties]
    return False if missing else True
