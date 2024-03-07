from App.config import getConfiguration
from collective.exportimport import config
from collective.exportimport import import_content
from collective.exportimport.import_content import ImportContent as BaseImportView
from pathlib import Path
from plone import api
from plone.dexterity.content import DexterityContent
from plone.dexterity.interfaces import IDexterityFTI
from plone.distribution import logger
from plone.distribution.exportimport import helpers
from plone.distribution.exportimport.interfaces import ExportFormat
from Products.Five import BrowserView
from typing import List
from zope.component import queryUtility


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
            import_content.BLOB_HOME = config.CENTRAL_DIRECTORY
        else:
            # Fallback to default (e.g. var/instance/import)
            cfg = getConfiguration()
            path = Path(cfg.clienthome) / "import"

        view = api.content.get_view(self.CONTENT_VIEW, self.context, request)
        request.form["form.submitted"] = True
        # Update the existing content using the update-strategy
        request.form["handle_existing_content"] = 2
        # Commit every 500 items
        request.form["commit"] = 500
        is_one_file = helpers.sniff_export_format(path) == ExportFormat.ONE_FILE
        if is_one_file:
            file_names = [
                "content.json",
                "portal.json",
            ]
            for file_name in file_names:
                view(server_file=file_name, return_json=True)
                logger.info(f"Imported {file_name[:-4]}")
        else:
            directory = path / "items"
            view(server_directory=directory, return_json=True)
            logger.info(f"Imported content from {directory}")

        other_imports = [step[0] for step in helpers.ALL_EXPORT_STEPS]
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
    portal_id: str

    def __call__(
        self,
        jsonfile=None,
        return_json=False,
        limit=None,
        server_file=None,
        iterator=None,
        server_directory=False,
    ):
        self.portal = api.portal.get()
        self.default_language = api.portal.get_registry_record(
            "plone.default_language", default="en"
        )
        self.languages = api.portal.get_registry_record(
            "plone.available_languages",
            default=[
                "en",
            ],
        )
        return super().__call__(
            jsonfile, return_json, limit, server_file, iterator, server_directory
        )

    def global_dict_hook(self, item: dict) -> dict:
        # Fix Language
        current = item.get("language")
        if current not in self.languages:
            item["language"] = self.default_language
        return item

    def dict_hook_plonesite(self, item: dict) -> dict:
        """The Plone Site object exists already so it is updated.
        We keep id and UID of the existing object."""
        item["UID"] = api.content.get_uuid(obj=self.portal)
        item["@id"] = f"/{self.portal.id}"
        item["id"] = self.portal.id
        item["title"] = self.portal.title
        item["description"] = self.portal.description
        return item

    def obj_hook_plonesite(self, obj: DexterityContent, item: dict) -> None:
        """IBlocks(obj) does not work yet at this point, so we have to
        force the blocks onto the object if Plone Site has the behavior.
        """
        fti = queryUtility(IDexterityFTI, name="Plone Site")
        if (
            fti
            and "volto.blocks" in fti.behaviors
            and "blocks" in item
            and "blocks_layout" in item
        ):
            obj.blocks = item["blocks"]
            obj.blocks_layout = item["blocks_layout"]
        return
