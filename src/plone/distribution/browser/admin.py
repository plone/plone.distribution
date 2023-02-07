from OFS.interfaces import IApplication
from plone.distribution.api import distribution as dist_api
from plone.distribution.api import site as site_api
from plone.distribution.core import Distribution
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFPlone.browser.admin import AddPloneSite as AddPloneSiteView
from Products.CMFPlone.browser.admin import AppTraverser
from zope.component import adapts
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IRequest

import json


class RestTraverser(AppTraverser):
    """Traverser supporting REST calls in Zope Application root."""

    adapts(IApplication, IRequest)

    def publishTraverse(self, request, name):
        if not name.startswith("@"):
            return super().publishTraverse(request, name)

        service = queryMultiAdapter(
            (self.context, request), name=request._rest_service_id + name
        )
        if service is None:
            # No service, fallback to regular view
            view = queryMultiAdapter((self.context, request), name=name)
            if view is not None:
                return view
            raise
        return service


class Overview(BrowserView):
    """Overview page for Zope Root."""


class AddPloneSite(AddPloneSiteView):
    """Add Plone site."""

    distribution: Distribution = None
    default_data: dict = None

    def __call__(self):
        context = self.context
        form = self.request.form
        distribution_name = form.get("distribution", "default")
        site_id = form.get("site_id")
        self.distribution = dist_api.get(distribution_name)
        submitted = form.get("form.submitted", False)
        if submitted:
            # CSRF protect. DO NOT use auto CSRF protection for adding a site
            alsoProvides(self.request, IDisableCSRFProtection)
            site = site_api.create(
                context,
                distribution_name,
                profile_id="Products.CMFPlone:plone",
                answers=form,
            )
            self.request.response.redirect(site.absolute_url())
            return ""
        else:
            self.default_data = json.dumps(
                {
                    "site_id": site_id,
                    "default_language": self.browser_language(),
                    "portal_timezone": "UTC",
                },
                indent=2,
            )
        return self.index()
