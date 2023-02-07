from zope.interface import Interface


class IDistributionRegistry(Interface):
    def register(distribution):
        """Register a distribution in the Distribution Registry."""

    def unregister(distribution):
        """Remove registration of a distribution in the Distribution Registry."""

    def clear():
        """Remove all distribution's registrations."""

    def lookup(name):
        """Return a named distribution."""

    def __getitem__(name):
        """Convenience spelling for `lookup(name)`."""

    def enumerate_distributions():
        """Return all distributions registered in the Distribution Registry."""


class IDistribution(Interface):
    """Named distribution."""
