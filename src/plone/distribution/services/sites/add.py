"""Service to create a Plone Site."""
from plone.distribution.api import site as site_api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import BadRequest
from zExceptions import NotFound
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import plone.protect.interfaces


@implementer(IPublishTraverse)
class SiteCreate(Service):
    def __init__(self, context, request):
        super().__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        # Consume any path segments after /@sites as parameters
        self.params.append(name)
        return self

    def reply(self):
        # Disable CSRF protection
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)
        data = json_body(self.request)
        distribution_name = (
            self.params[0] if self.params else data.get("distribution", "default")
        )
        self.errors = []
        # self.validate_input_data(portal, data)
        # Create site
        try:
            site = site_api.create(
                self.context,
                distribution_name=distribution_name,
                answers=data,
            )
        except ValueError:
            raise NotFound(f"No distribution named {distribution_name}.")
        except KeyError:
            raise BadRequest("Error creating the site.")
        site_info = {
            "@id": site.absolute_url(),
            "id": site.id,
            "title": site.title,
            "description": site.description,
        }
        return site_info
