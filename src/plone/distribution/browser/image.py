from plone.distribution.api import distribution as dist_api
from zExceptions import NotFound
from zope.interface import implementer
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class DistributionImageView(BrowserView):
    def __init__(self, context, request):
        super().__init__(context, request)

    def publishTraverse(self, request, name):
        request["TraversalRequestNameStack"] = []
        self.path = name
        distribution_name = name.replace(".png", "")
        self.distribution = dist_api.get(distribution_name)
        if not self.distribution:
            raise NotFound(self.context)
        return self

    def set_headers(self, data, response):
        """Set response headers for the given file. If filename is given, set
        the Content-Disposition to attachment.
        """
        contenttype = "image/png"
        response.setHeader("Content-Type", contenttype)
        response.setHeader("Content-Length", len(data))

    def __call__(self):
        request = self.request
        distribution = self.distribution
        image = distribution.image
        data = image.read_bytes()
        self.set_headers(data, request.response)
        return data
