from pathlib import Path
from plone import api
from plone.distribution.core import Distribution
from plone.distribution.core import SiteCreationReport
from plone.distribution.registry import _distribution_registry
from plone.distribution.registry import DistributionRegistry
from Products.CMFPlone.Portal import PloneSite
from typing import List
from typing import Optional
from typing import Union
from zope.annotation.interfaces import IAnnotations

import os


base_folder = Path(__file__).parent.parent / "distributions"
SITE_REPORT_ANNO = "__plone_distribution_report__"


def _allow_list() -> List[str]:
    """Return a list of allowed distributions."""
    allowed_distributions = os.environ.get("ALLOWED_DISTRIBUTIONS", "")
    if allowed_distributions:
        allowed_distributions = allowed_distributions.split(",")
    return allowed_distributions


def get_registry() -> DistributionRegistry:
    """Return the Distribution Registry.

    :returns: Distribution Registry instance.

    :Example: :ref:`api-distribution-get_registry-example`
    """
    return _distribution_registry


def get_distributions(filter: bool = True) -> List[Distribution]:
    """Get available Plone distributions.

    :param filter: Return only registered Distributions that
                   are also listed on **ALLOWED_DISTRIBUTIONS**
                   environment variable.
    :returns: List of registered distributions.

    :Example: :ref:`api-distribution-get_distributions-example`
    """
    registry = get_registry()
    all_distributions = registry.enumerate_distributions()
    allowed_distributions = _allow_list()
    if filter and allowed_distributions:
        return [d for d in all_distributions if d.name in allowed_distributions]
    return all_distributions


def get(name: str) -> Distribution:
    """Get a distribution.

    :param name: Distribution name.
    :raises:
        :class:`ValueError`,
    :returns: A Plone Distribution

    :Example: :ref:`api-distribution-get-example`
    """
    registry = get_registry()
    distribution = registry.lookup(name)
    if not distribution:
        raise ValueError(f"No distribution named {name}")
    return distribution


def get_creation_report(site: PloneSite) -> Union[SiteCreationReport, None]:
    """Return a site creation report for a Plone site.

    :param site: Plone Site.
    :returns: SiteCreationReport with distribution name, creation date and
              answers used to create the site.

    :Example: :ref:`api-distribution-get_creation_report-example`
    """
    annotations = IAnnotations(site)
    return annotations.get(SITE_REPORT_ANNO, None)


def get_current_distribution(site: PloneSite = None) -> Optional[Distribution]:
    """Get the distribution used to create the current site."""
    if site is None:
        site = api.portal.get()
    creation_report = get_creation_report(site)
    dist = None
    if creation_report:
        name = creation_report.name or creation_report.answers.get("distribution", "")
        dist = get(name=name)
    return dist
