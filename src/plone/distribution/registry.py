from AccessControl.class_init import InitializeClass
from AccessControl.SecurityInfo import ClassSecurityInfo
from Acquisition import Implicit
from plone.distribution.core import Distribution
from plone.distribution.interfaces import IDistribution
from plone.distribution.interfaces import IDistributionRegistry
from typing import Any
from typing import List
from typing import Tuple
from zope.component import getGlobalSiteManager
from zope.interface import implementer
from zope.interface import Interface


ManagePortal = "Manage Site"


class GlobalRegistryStorage:
    """Helper to manage Registry access."""

    def __init__(self, interfaceClass: Interface):
        self.interfaceClass = interfaceClass

    def keys(self) -> List[str]:
        """Return a list of names of all registered utilities."""
        sm = getGlobalSiteManager()
        return [n for n, _i in sm.getUtilitiesFor(self.interfaceClass)]

    def values(self) -> List[Any]:
        """Return a list with all registered utilities."""
        sm = getGlobalSiteManager()
        return [i for _n, i in sm.getUtilitiesFor(self.interfaceClass)]

    def items(self) -> List[Tuple[str, Any]]:
        """Return a list with all registered utilities as tuples.

        Each tuple contains name, utility.
        """
        sm = getGlobalSiteManager()
        return [(n, i) for n, i in sm.getUtilitiesFor(self.interfaceClass)]

    def get(self, key: str) -> Any:
        """Return a registered utility by name."""
        sm = getGlobalSiteManager()
        return sm.queryUtility(provided=self.interfaceClass, name=key)

    def __setitem__(self, id: str, info: Any) -> None:
        """Register a named utility."""
        sm = getGlobalSiteManager()
        return sm.registerUtility(info, provided=self.interfaceClass, name=id)

    def __delitem__(self, id: str) -> bool:
        """Remove a registration for a named utility."""
        sm = getGlobalSiteManager()
        return sm.unregisterUtility(provided=self.interfaceClass, name=id)

    def clear(self) -> None:
        """Remove all registration of named utilities."""
        for key in self.keys():
            del self[key]


@implementer(IDistributionRegistry)
class DistributionRegistry(Implicit):
    """Track Registered Distributions."""

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

    def __init__(self):
        """Initialize the Distribution Registration"""
        self._registered = GlobalRegistryStorage(IDistribution)
        self.clear()

    @security.protected(ManagePortal)
    def register(self, distribution: Distribution):
        """Register a distribution in the Distribution Registry."""
        self._registered[distribution.name] = distribution

    @security.protected(ManagePortal)
    def unregister(self, distribution: Distribution):
        """Remove registration of a distribution in the Distribution Registry."""
        del self._registered[distribution.name]

    @security.private
    def clear(self):
        """Remove all distribution's registrations."""
        self._registered.clear()

    @security.protected(ManagePortal)
    def lookup(self, name: str) -> Distribution:
        """Return a named distribution."""
        return self._registered.get(name)

    @security.protected(ManagePortal)
    def __getitem__(self, name) -> Distribution:
        """Convenience spelling for `lookup(name)`."""
        return self.lookup(name)

    @security.protected(ManagePortal)
    def enumerate_distributions(self) -> List[Distribution]:
        """Return all distributions registered in the Distribution Registry.

        This implementation returns the distributions sorted by name, but keep
        the distribution named default as the first item of the list.
        """
        result = []
        distributions = sorted(self._registered.items())
        for name, distribution in distributions:
            if name == "default":
                result.insert(0, distribution)
            else:
                result.append(distribution)
        return tuple(result)


InitializeClass(DistributionRegistry)

_distribution_registry = DistributionRegistry()
