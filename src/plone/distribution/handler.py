from plone import api
from plone.dexterity.schema import SCHEMA_CACHE
from plone.distribution import logger
from plone.distribution.core import Distribution
from plone.distribution.utils.data import convert_data_uri_to_b64
from plone.exportimport.importers import get_importer
from Products.CMFPlone.Portal import PloneSite

import transaction


def default_pre_handler(answers: dict) -> dict:
    """Process answers before creating a new site."""
    return answers


def default_handler(
    distribution: Distribution, site: PloneSite, answers: dict
) -> PloneSite:
    """Default handler to create a new site."""
    # Process answers
    profiles = distribution.profiles
    setup_content = answers.get("setup_content", False)
    setup_tool = site["portal_setup"]
    for profile_id in profiles:
        setup_tool.runAllImportStepsFromProfile(f"profile-{profile_id}")

    # Add default content if needed
    if setup_content:
        # If there is no savepoint most tests fail with a PosKeyError
        transaction.savepoint(optimistic=True)
        contents = distribution.contents
        # First process any content profiles
        content_profiles = contents["profiles"]
        for profile_id in content_profiles:
            setup_tool.runAllImportStepsFromProfile(f"profile-{profile_id}")
        # Process content import from json
        content_json_path = contents["json"]
        if content_json_path:
            # Invalidate the schema cache to make sure we get up to date behaviors.
            # Normally this happens on commit, but we didn't commit yet.
            SCHEMA_CACHE.clear()
            importer = get_importer(site)
            importer.import_site(content_json_path)
            # Create a savepoint to ensure the import is atomic
            transaction.savepoint(optimistic=True)
            # Commit the transaction to finalize the import
            transaction.commit()
    return site


def post_handler(
    distribution: Distribution, site: PloneSite, answers: dict
) -> PloneSite:
    """After site creation, run last steps."""
    name = distribution.name
    raw_logo = answers.get("site_logo")
    if raw_logo:
        logo = convert_data_uri_to_b64(raw_logo)
        logger.info(f"{name}: Set logo")
        api.portal.set_registry_record("plone.site_logo", logo)
    return site
