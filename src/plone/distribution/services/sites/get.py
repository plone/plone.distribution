from AccessControl import getSecurityManager
from plone.distribution.api import distribution as dist_api
from plone.distribution.api import site as site_api
from plone.distribution.utils.request import extract_browser_language
from plone.restapi.services import Service
from Products.CMFCore.permissions import ManagePortal
from typing import List
from zExceptions import BadRequest
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json


DEFAULT_ID = "Plone"


def _is_outdated(site) -> bool:
    """Check if site needs an upgrade."""
    mig = getattr(site, "portal_migration", None) or site.get("portal_migration", None)
    return mig.needUpgrading() if mig else False


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
        for site in sites:
            response.append(
                {
                    "@id": site.absolute_url(),
                    "id": site.id,
                    "title": site.title,
                    "description": site.description,
                    "creation_date": site.CreationDate(),
                    "needs_upgrade": _is_outdated(site),
                }
            )
        return response

    def _populate_server_defaults(self) -> dict:
        """Provide default values for new Plone sites."""
        request = self.request
        # Sites with default id
        all_sites = self.get_sites()
        sites = [site for site in all_sites if site["id"].startswith(DEFAULT_ID)]
        site_id = f"{DEFAULT_ID}{len(sites)}" if sites else DEFAULT_ID
        language = extract_browser_language(request)
        return {
            "site_id": site_id,
            "default_language": language,
        }

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
                "default_values": self._populate_server_defaults(),
            }
