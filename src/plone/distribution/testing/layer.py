from copy import deepcopy
from plone.app.testing.interfaces import PLONE_SITE_ID
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
from plone.app.testing.interfaces import TEST_USER_ID
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.app.testing.interfaces import TEST_USER_PASSWORD
from plone.app.testing.interfaces import TEST_USER_ROLES
from plone.app.testing.layers import PloneFixture
from plone.testing import zope


DEFAULT_DISTRIBUTION = "default"
DEFAULT_ANSWERS = {
    "site_id": PLONE_SITE_ID,
    "title": "Plone Site",
    "description": "A Plone Site",
    "default_language": "en",
    "portal_timezone": "America/Sao_Paulo",
    "setup_content": True,
}


class PloneDistributionFixture(PloneFixture):
    """Base Fixture to test plone distributions.

    This Fixture should be extended before being used.
    """

    PACKAGE_NAME: str = ""
    SITES: tuple = ()

    _distribution_products = (
        ("plone.app.contenttypes", {"loadZCML": True}),
        ("plone.restapi", {"loadZCML": True}),
        ("collective.exportimport", {"loadZCML": True}),
        ("plone.volto", {"loadZCML": True, "silent": True}),
        ("plone.distribution", {"loadZCML": True}),
    )

    @property
    def products(self):
        """Merge products available on PloneFixture, with ones needed here."""
        products = []
        products.extend([p for p in super().products])
        products.extend([p for p in self._distribution_products])
        if self.PACKAGE_NAME:
            products.append((self.PACKAGE_NAME, {"loadZCML": True}))
        return tuple(products)

    @property
    def sites(self):
        """Guarantee there is at least one site created."""
        sites = self.SITES
        if not sites:
            sites = ((DEFAULT_DISTRIBUTION, deepcopy(DEFAULT_ANSWERS)),)
        return sites

    def setUpDefaultContent(self, app):
        """Create a Plone site using plone.distribution."""
        from plone.distribution.api import site as site_api

        # Create the owner user and "log in" so that the site object gets
        # the right ownership information
        app["acl_users"].userFolderAddUser(
            SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ["Manager"], []
        )

        zope.login(app["acl_users"], SITE_OWNER_NAME)
        sites = self.sites
        for distribution_name, answers in sites:
            site_id = answers["site_id"]
            # Create Plone site
            site_api.create(
                context=app, distribution_name=distribution_name, answers=answers
            )

            # Create the test user. (Plone)PAS does not have an API to create a
            # user with different userid and login name, so we call the plugin
            # directly.
            pas = app[site_id]["acl_users"]
            pas.source_users.addUser(TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD)
            for role in TEST_USER_ROLES:
                pas.portal_role_manager.doAssignRoleToPrincipal(TEST_USER_ID, role)

        # Log out again
        zope.logout()
