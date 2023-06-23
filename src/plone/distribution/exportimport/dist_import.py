from App.config import getConfiguration
from collective.exportimport import config
from collective.exportimport import import_content
from collective.exportimport.import_content import ImportContent as BaseImportView
from logging import getLogger
from pathlib import Path
from plone import api
from Products.Five import BrowserView
from typing import List


logger = getLogger(__name__)


class ImportAll(BrowserView):
    """View to import distribution content."""

    CONTENT_VIEW: str = "dist_import_content"

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

        view = api.content.get_view(self.CONTENT_VIEW, self.context, request)
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


class ImportContent(BaseImportView):
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
