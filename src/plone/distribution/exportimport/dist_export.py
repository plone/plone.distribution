from collective.exportimport import config
from collective.exportimport.export_content import ExportContent as BaseExportView
from logging import getLogger
from plone import api
from plone.distribution.core import Distribution
from plone.distribution.exportimport.helpers import filter_devel_distributions
from plone.distribution.exportimport.helpers import parse_blocks
from plone.distribution.exportimport.helpers import remove_site_root
from plone.distribution.exportimport.interfaces import IDistributionBlobsMarker
from Products.Five import BrowserView
from typing import List
from zope.interface import alsoProvides


logger = getLogger(__name__)


class ExportAll(BrowserView):
    def __call__(self):
        distribution = None
        request = self.request
        if not request.form.get("form.submitted", False):
            return self.index()

        dist_name = request.form.get("distribution", "")
        distributions = self.distributions(dist_name)
        if not distributions:
            api.portal.show_message("Please select a valid target")
            return self.index()
        distribution = distributions[0]
        alsoProvides(self.request, IDistributionBlobsMarker)
        package_path = distribution.directory
        directory = package_path / "content"
        config.CENTRAL_DIRECTORY = str(directory)
        # pass the target-dir to blob-serializer via request
        request.form["distribution_directory"] = str(directory)

        # Export all content
        export_name = "dist_export_content"
        view = api.content.get_view(export_name, self.context, request)
        # small hack to get all exportable types from the view
        view.portal_type = []
        view.path = "/".join(self.context.getPhysicalPath())
        view.depth = -1
        portal_types = [
            i["value"] for i in view.portal_types() if i["value"] != "Plone Site"
        ]
        request.form["filename"] = "content.json"
        view(portal_type=portal_types, include_blobs=2, download_to_server=True)
        logger.info(f"Finished {export_name}")

        portal_types = ["Plone Site"]
        request.form["filename"] = "portal.json"
        # To handle an issue with json_body deserialization
        request["BODY"] = {}
        view(portal_type=portal_types, include_blobs=2, download_to_server=True)
        logger.info(f"Finished {export_name}")

        other_exports = [
            "relations",
            "members",
            "translations",
            "localroles",
            "ordering",
            "defaultpages",
            "discussion",
            "portlets",
            "redirects",
        ]
        for export in other_exports:
            export_view = api.content.get_view(
                f"export_{export}", self.context, request
            )
            request.form["form.submitted"] = True
            request.form["filename"] = f"{export}.json"
            export_view(download_to_server=True)

        logger.info("Finished export_all")
        return self.request.response.redirect(self.context.absolute_url())

    def distributions(self, name: str = "") -> List[Distribution]:
        """Return a list of distributions."""
        return filter_devel_distributions(name=name)


class ExportContent(BaseExportView):
    """Export content from a distribution."""

    PORTAL_URL: str = ""

    def __call__(
        self,
        portal_type=None,
        path=None,
        depth=-1,
        include_blobs=1,
        download_to_server=False,
        migration=True,
        include_revisions=False,
    ):
        self.PORTAL_URL = api.portal.get().absolute_url()
        return super().__call__(
            portal_type,
            path,
            depth,
            include_blobs,
            download_to_server,
            migration,
            include_revisions,
        )

    def global_dict_hook(self, item, obj):
        """Clean up data before export."""
        item = remove_site_root(item)
        if item["@type"] == "Plone Site":
            # To avoid a conflict between @id and id
            item["@id"] = f"/{item['id']}"
        if "blocks" in item:
            blocks = item["blocks"]
            item["blocks"] = parse_blocks(blocks)
        return item
