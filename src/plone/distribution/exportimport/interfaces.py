"""Module where all interfaces, events and exceptions live."""
from collective.exportimport.interfaces import IPathBlobsMarker


class IDistributionBlobsMarker(IPathBlobsMarker):
    """A marker interface to override default serializers."""
