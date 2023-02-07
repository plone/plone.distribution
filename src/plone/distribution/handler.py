from plone.distribution.core import Distribution
from Products.CMFPlone.Portal import PloneSite


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
        contents = distribution.contents
        # First process any content profiles
        content_profiles = contents["profiles"]
        for profile_id in content_profiles:
            setup_tool.runAllImportStepsFromProfile(f"profile-{profile_id}")
        # Process content import from json
        content_json_path = contents["json"]
        if content_json_path:
            # TODO: Import content
            pass
    return site
