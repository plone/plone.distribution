from AccessControl import getSecurityManager
from AccessControl.Permissions import view as View
from datetime import datetime
from datetime import timezone
from plone.base.interfaces import IPloneSiteRoot
from plone.distribution.api import distribution as dist_api
from plone.distribution.core import SiteCreationReport
from plone.distribution.handler import default_handler
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.events import SiteManagerCreatedEvent
from Products.CMFPlone.Portal import PloneSite
from Products.GenericSetup.tool import SetupTool
from typing import List
from typing import Union
from ZODB.broken import Broken
from zope.annotation.interfaces import IAnnotations
from zope.component import queryUtility
from zope.component.hooks import setSite
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent


_TOOL_ID = "portal_setup"
_DEFAULT_PROFILE = "Products.CMFPlone:plone"


SITE_REPORT_ANNO = "__plone_distribution_report__"


def _required_str_value(answers: dict, key: str) -> str:
    try:
        return answers[key]
    except KeyError:
        raise KeyError(f"A value for {key} is required.")


def get_sites(context=None) -> List[PloneSite]:
    """Get all Plone sites.

    :param context: Base context to search for Plone Sites.
    :raises:
        :class:`ValueError`,
    :returns: A list of Plone Sites

    :Example: :ref:`api-site-get_sites-example`
    """
    if not context:
        raise ValueError("Need to provide application root")
    result = []
    secman = getSecurityManager()
    candidates = (obj for obj in context.values() if not isinstance(obj, Broken))
    for obj in candidates:
        if obj.meta_type == "Folder":
            result.extend(get_sites(context=obj))
        elif IPloneSiteRoot.providedBy(obj):
            if secman.checkPermission(View, obj):
                result.append(obj)
        elif obj.getId() in getattr(context, "_mount_points", {}):
            result.extend(get_sites(context=obj))
    return result


def get_creation_report(site: PloneSite) -> Union[SiteCreationReport, None]:
    """Return a site creation report for a Plone site.

    :param site: Plone Site.
    :returns: SiteCreationReport with distribution name, creation date and
              answers used to create the site.

    :Example: :ref:`api-site-get_creation_report-example`
    """
    annotations = IAnnotations(site)
    return annotations.get(SITE_REPORT_ANNO, None)


def create(
    context,
    distribution_name: str,
    answers: dict,
    profile_id: str = _DEFAULT_PROFILE,
) -> PloneSite:
    """Create a new Plone site using one of the distributions.

    :param context: Context where the site will be created.
    :param distribution_name: Name of distribution to be used.
    :param answers: Payload for site creation.
    :param profile_id: Base profile to be used.
                       default: `Products.CMFPlone:plone`
    :raises:
        :class:`ValueError`,
        :class:`KeyError`,
    :returns: Created Plone Site

    :Example: :ref:`api-site-create-example`
    """
    distribution = dist_api.get(distribution_name)
    handler = distribution.handler if distribution.handler else default_handler
    post_handler = distribution.post_handler
    # Attributes used during site creation
    site_id = _required_str_value(answers, "site_id")
    title = _required_str_value(answers, "title")
    description = answers.get("description", "")
    default_language = answers.get("default_language", "en")
    portal_timezone = answers.get("portal_timezone", "UTC")
    # Create the Plone Site
    site = PloneSite(site_id)
    notify(ObjectCreatedEvent(site))
    context[site_id] = site
    site = context[site_id]
    # Set site language
    site.setLanguage(default_language)
    # Register SetupTool (portal_setup)
    site[_TOOL_ID] = SetupTool(_TOOL_ID)
    setup_tool = site[_TOOL_ID]
    notify(SiteManagerCreatedEvent(site))
    setSite(site)
    # Apply base profile
    setup_tool.setBaselineContext(f"profile-{profile_id}")
    setup_tool.runAllImportStepsFromProfile(f"profile-{profile_id}")
    # Set default properties (title, description)
    # Do this before applying extension profiles, so the settings from a
    # properties.xml file are applied and not overwritten by this
    props = dict(
        title=title,
        description=description,
    )
    site.manage_changeProperties(**props)
    # Set initial registry values
    reg = queryUtility(IRegistry, context=site)
    reg["plone.portal_timezone"] = portal_timezone
    reg["plone.available_timezones"] = [portal_timezone]
    reg["plone.default_language"] = default_language
    reg["plone.available_languages"] = [default_language]
    reg["plone.site_title"] = title
    # Run the Distribution handler
    site = handler(distribution, site, answers)
    # Run the Distribution post_handler
    if post_handler:
        site = post_handler(distribution, site, answers)
    # Create a report of a site creation
    annotations = IAnnotations(site)
    report = SiteCreationReport(
        distribution_name, datetime.now(tz=timezone.utc), answers
    )
    annotations[SITE_REPORT_ANNO] = report
    return site
