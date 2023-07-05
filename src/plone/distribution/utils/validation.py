from jsonschema import exceptions
from jsonschema import validate
from plone.distribution import logger


def validate_answers(answers: dict, schema: dict) -> bool:
    """Validate answers against the provided schema.

    :param answers: Payload for site creation.
    :param schema: A JSON Schema.

    :returns: Boolean indicating if the answers are valid or not.
    """
    is_valid = False
    try:
        validate(instance=answers, schema=schema)
    except exceptions.ValidationError as exc:
        logger.exception("Validation error", exc_info=exc)
    except (exceptions.SchemaError, exceptions.RefResolutionError) as exc:
        logger.exception("Schema error", exc_info=exc)
    else:
        site_id = answers.get("site_id").strip()
        title = answers.get("title").strip()
        is_valid = True if site_id and title else False
    return is_valid
