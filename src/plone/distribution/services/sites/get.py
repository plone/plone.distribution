from AccessControl import getSecurityManager
from plone.distribution.api import distribution as dist_api
from plone.distribution.api import site as site_api
from plone.distribution.core import Distribution
from plone.distribution.utils.request import extract_browser_language
from plone.distribution.utils.schema import should_provide_default_language_default
from plone.restapi.services import Service
from Products.CMFCore.permissions import ManagePortal
from Products.CMFPlone.Portal import PloneSite
from typing import List
from zExceptions import BadRequest
from zope.component.hooks import site
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json


DEFAULT_ID = "Plone"


def _is_outdated(plone_site: PloneSite) -> bool:
    """Check if a Portal needs to be upgraded."""
    with site(plone_site):
        mig = getattr(plone_site, "portal_migration", None) or plone_site.get(
            "portal_migration", None
        )
        is_outdated = mig.needUpgrading() if mig else False
    return is_outdated


_no_content_marker = object()


@implementer(IPublishTraverse)
class SitesGet(Service):
    def __init__(self, context, request):
        super().__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        # Consume any path segments after /@users as parameters
        self.params.append(name)
        return self

    def check_permission(self):
        """Ignore 'plone.restapi: Use REST API' permission on Application."""
        pass

    def render(self):
        # Make sure we do not change the order of the keys
        content = self.reply()
        if content is not _no_content_marker:
            self.request.response.setHeader("Content-Type", self.content_type)
            return json.dumps(content, indent=2, separators=(", ", ": "))

    def get_distributions(self, base_url: str) -> List[dict]:
        """Return a list of available distributions."""
        response = []
        distributions = dist_api.get_distributions()
        for dist in distributions:
            response.append(
                {
                    "@id": f"{base_url}/{dist.name}",
                    "name": dist.name,
                    "title": dist.title,
                    "description": dist.description,
                    "image": f"{self.context.absolute_url()}/@@dist-image/{dist.name}",
                }
            )
        return response

    def get_sites(self) -> List[dict]:
        """Return a list of site information."""
        response = []
        sites = site_api.get_sites(self.context)
        for plone_site in sites:
            dist_report = dist_api.get_creation_report(plone_site)
            distribution_name = dist_report.name if dist_report else ""
            response.append(
                {
                    "@id": plone_site.absolute_url(),
                    "id": plone_site.id,
                    "title": plone_site.title,
                    "description": plone_site.description,
                    "creation_date": plone_site.CreationDate(),
                    "needs_upgrade": _is_outdated(plone_site),
                    "distribution": distribution_name,
                }
            )
        return response

    def _populate_server_defaults(self, distribution: Distribution) -> dict:
        """Provide default values for new Plone sites."""
        server_defaults = {}
        request = self.request
        # Sites with default id
        all_sites = self.get_sites()
        site_ids = [
            site["id"] for site in all_sites if site["id"].startswith(DEFAULT_ID)
        ]
        if site_ids:
            count = len(site_ids)
            new_site_id = f"{DEFAULT_ID}{count}"
            while new_site_id in site_ids:
                count += 1
                new_site_id = f"{DEFAULT_ID}{count}"
        else:
            new_site_id = DEFAULT_ID
        server_defaults["site_id"] = new_site_id
        jsonschema = distribution.schema
        uischema = distribution.uischema
        if should_provide_default_language_default(uischema, jsonschema):
            server_defaults["default_language"] = extract_browser_language(request)
        return server_defaults

    def can_manage(self) -> bool:
        secman = getSecurityManager()
        return True if secman.checkPermission(ManagePortal, self.context) else False

    def reply(self) -> dict:
        base_url = f"{self.context.absolute_url()}/@sites"
        if len(self.params) == 0:
            return {
                "@id": base_url,
                "can_manage": self.can_manage(),
                "sites": self.get_sites(),
                "distributions": self.get_distributions(base_url),
            }
        else:
            name = self.params[0]
            dist = dist_api.get(name)
            if not dist:
                raise BadRequest("Parameters supplied are not valid")
            return {
                "@id": f"{base_url}/{dist.name}",
                "name": dist.name,
                "title": dist.title,
                "description": dist.description,
                "image": f"{base_url}/@@dist-image/{dist.name}",
                "schema": dist.schema,
                "uischema": dist.uischema,
                "default_values": self._populate_server_defaults(dist),
            }
