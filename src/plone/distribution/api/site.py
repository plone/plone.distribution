from AccessControl import getSecurityManager
from AccessControl.Permissions import view as View
from datetime import datetime
from datetime import timezone
from plone.base.interfaces import IPloneSiteRoot
from plone.distribution import DEFAULT_PROFILE
from plone.distribution.api import distribution as dist_api
from plone.distribution.core import Distribution
from plone.distribution.core import SiteCreationReport
from plone.distribution.handler import default_handler
from plone.distribution.handler import default_pre_handler
from plone.distribution.utils.validation import validate_answers
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.events import SiteManagerCreatedEvent
from Products.CMFPlone.Portal import PloneSite
from Products.GenericSetup.tool import SetupTool
from typing import List
from ZODB.broken import Broken
from zope.annotation.interfaces import IAnnotations
from zope.component import queryUtility
from zope.component.hooks import setSite
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent

import transaction


_TOOL_ID = "portal_setup"


def _handlers_for_distribution(distribution: Distribution):
    """Return pre_handler, handler and post_handler for a distribution."""
    pre_handler = (
        distribution.pre_handler if distribution.pre_handler else default_pre_handler
    )
    handler = distribution.handler if distribution.handler else default_handler
    return pre_handler, handler, distribution.post_handler


def _create_bare_site(context, answers: dict, profile_id: str) -> PloneSite:
    """Create a Plone site."""
    site_id = answers.get("site_id")
    title = answers.get("title")
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
    props = {
        "title": title,
        "description": description,
    }
    site.manage_changeProperties(**props)
    # Set initial registry values
    reg = queryUtility(IRegistry, context=site)
    reg["plone.portal_timezone"] = portal_timezone
    reg["plone.available_timezones"] = [portal_timezone]
    reg["plone.default_language"] = default_language
    reg["plone.available_languages"] = [default_language]
    reg["plone.site_title"] = title
    return site


def _add_report_to_site(site: PloneSite, distribution_name: str, answers: dict) -> None:
    """Add a report to the newly created site."""
    # Create a report of a site creation
    annotations = IAnnotations(site)
    report = SiteCreationReport(
        distribution_name, datetime.now(tz=timezone.utc), answers
    )
    annotations[dist_api.SITE_REPORT_ANNO] = report


def _create_site(
    context,
    distribution_name: str,
    answers: dict,
) -> PloneSite:
    """Create site"""
    distribution = dist_api.get(distribution_name)
    pre_handler, handler, post_handler = _handlers_for_distribution(distribution)
    profile_id = distribution.profile_id
    # Process answers
    answers = pre_handler(answers)
    # Create base site
    site = _create_bare_site(context, answers, profile_id)
    # Run the Distribution handler
    site = handler(distribution, site, answers)
    # Run the Distribution post_handler
    if post_handler:
        site = post_handler(distribution, site, answers)
    # Create a report of a site creation
    _add_report_to_site(site, distribution_name, answers)
    return site


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


def create(
    context,
    distribution_name: str,
    answers: dict,
    profile_id: str = DEFAULT_PROFILE,
) -> PloneSite:
    """Create a new Plone site using one of the distributions.

    :param context: Context where the site will be created.
    :param distribution_name: Name of distribution to be used.
    :param answers: Payload for site creation.
    :param profile_id: (deprecated and ignored) Base profile to be used.
                       default: `Products.CMFPlone:plone`
    :raises:
        :class:`ValueError`,
        :class:`KeyError`,
    :returns: Created Plone Site

    :Example: :ref:`api-site-create-example`
    """
    distribution = dist_api.get(distribution_name)
    # Validate answers
    schema = distribution.schema
    if not validate_answers(answers=answers, schema=schema):
        raise ValueError("Provided answers are not valid")
    with transaction.manager as tm:
        site = _create_site(context, distribution_name, answers)
        tm.note(f"Plone site {site.getId()} created with {distribution_name}")
    return site
