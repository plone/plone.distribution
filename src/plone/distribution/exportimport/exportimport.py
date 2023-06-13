from App.config import getConfiguration
from collective.exportimport import config
from collective.exportimport import import_content
from collective.exportimport.import_content import ImportContent as BaseView
from logging import getLogger
from pathlib import Path
from plone import api
from plone.distribution.api import distribution as dist_api
from plone.distribution.exportimport.interfaces import IDistributionBlobsMarker
from Products.Five import BrowserView
from typing import List
from zope.interface import alsoProvides


logger = getLogger(__name__)


class ImportAll(BrowserView):
    def __call__(self, path=None):
        request = self.request
        if not path and not request.form.get("form.submitted", False):
            return self.index()
        elif path:
            # path the config that is usually set via env-variables
            config.CENTRAL_DIRECTORY = str(path)
            import_content.BLOB_HOME = str(path)
        else:
            # Fallback to default (e.g. var/instance/import)
            cfg = getConfiguration()
            path = Path(cfg.clienthome) / "import"

        view = api.content.get_view("import_content", self.context, request)
        request.form["form.submitted"] = True
        # Add content
        request.form["commit"] = 500
        view(server_file="content.json", return_json=True)

        # Update the existing portal obj using the update-strategy
        request.form["handle_existing_content"] = 2
        view(server_file="portal.json", return_json=True)

        other_imports = [
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
        for name in other_imports:
            view = api.content.get_view(f"import_{name}", self.context, request)
            importfile = path / f"{name}.json"
            if importfile.exists():
                results = view(jsonfile=importfile.read_text(), return_json=True)
                logger.info(results)
            else:
                logger.info(f"Skipping import of {name} because no file {importfile}")

        return request.response.redirect(self.context.absolute_url())


class ExportAll(BrowserView):
    def __call__(self):
        request = self.request
        if not request.form.get("form.submitted", False):
            return self.index()

        dist_name = request.form.get("distribution", False)
        if not dist_name:
            api.portal.show_message("Please select a target")
            return self.index()

        alsoProvides(self.request, IDistributionBlobsMarker)
        distribution = dist_api.get(dist_name)
        package_path = distribution.directory
        directory = package_path / "content"
        config.CENTRAL_DIRECTORY = str(directory)
        # pass the target-dir to blob-serializer via request
        request.form["distribution_directory"] = str(directory)

        # Export all content
        export_name = "export_content"
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

    def distributions(self):
        return dist_api.get_distributions()


class ImportContent(BaseView):
    languages: List[str]
    default_language: str

    def __call__(
        self,
        jsonfile=None,
        return_json=False,
        limit=None,
        server_file=None,
        iterator=None,
    ):
        self.default_language = api.portal.get_registry_record(
            "plone.default_language", default="en"
        )
        self.languages = api.portal.get_registry_record(
            "plone.available_languages",
            default=[
                "en",
            ],
        )
        return super().__call__(jsonfile, return_json, limit, server_file, iterator)

    def global_dict_hook(self, item):
        # Fix Language
        current = item.get("language")
        if current not in self.languages:
            item["language"] = self.default_language
        return item
