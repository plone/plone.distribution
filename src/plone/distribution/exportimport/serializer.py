from pathlib import Path
from plone.dexterity.interfaces import IDexterityContent
from plone.distribution.exportimport.interfaces import IDistributionBlobsMarker
from plone.namedfile.interfaces import INamedFileField
from plone.namedfile.interfaces import INamedImageField
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxfields import DefaultFieldSerializer
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import implementer

import logging


logger = logging.getLogger(__name__)


@adapter(INamedFileField, IDexterityContent, IDistributionBlobsMarker)
@implementer(IFieldSerializer)
class DistributionFileFieldSerializer(DefaultFieldSerializer):
    def __call__(self):
        namedfile = self.field.get(self.context)
        if namedfile is None:
            return None
        blob_path = export_blob(
            self.context.UID(), self.field.__name__, namedfile.filename, namedfile.data
        )
        result = {
            "filename": namedfile.filename,
            "content-type": namedfile.contentType,
            "size": namedfile.getSize(),
            "blob_path": blob_path,
        }
        return json_compatible(result)


@adapter(INamedImageField, IDexterityContent, IDistributionBlobsMarker)
@implementer(IFieldSerializer)
class DistributionImageFieldSerializer(DefaultFieldSerializer):
    def __call__(self):
        namedfile = self.field.get(self.context)
        if namedfile is None:
            return None
        blob_path = export_blob(
            self.context.UID(), self.field.__name__, namedfile.filename, namedfile.data
        )
        width, height = namedfile.getImageSize()
        result = {
            "filename": namedfile.filename,
            "content-type": namedfile.contentType,
            "size": namedfile.getSize(),
            "width": width,
            "height": height,
            "blob_path": blob_path,
        }
        return json_compatible(result)


def export_blob(uid, fieldname, filename, data):
    """Store blob data in a way that makes it easier to edit by hand:
    <distribution>/content/blobs/<uid>-<fieldname>/<filename>"""
    unique_dir_name_for_file = f"{uid}-{fieldname}"
    request = getRequest()
    distribution_directory = Path(request["distribution_directory"])
    target_directory = distribution_directory / "blobs" / unique_dir_name_for_file
    if not target_directory.exists():
        target_directory.mkdir(parents=True)
    target_file = target_directory / filename
    with open(target_file, "wb") as f:
        f.write(data)
    return f"blobs/{unique_dir_name_for_file}/{filename}"
