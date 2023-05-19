from plone import api
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.component.hooks import setSite

import pytest


@pytest.fixture()
def portal(portal_classic):
    setSite(portal_classic)
    return portal_classic


class TestDistributionDefault:
    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "Plone Site"),
            ("description", "A Plone Site with Classic UI"),
            ("exclude_from_nav", False),
        ],
    )
    def test_plone_site_attributes(self, portal, attr, expected):
        assert getattr(portal, attr) == expected

    @pytest.mark.parametrize(
        "package,expected",
        [
            ("plone.app.contenttypes", True),
            ("plone.app.caching", True),
            ("plonetheme.barceloneta", True),
            ("plone.restapi", False),
            ("plone.volto", False),
        ],
    )
    def test_dependencies_installed(self, installer, package, expected):
        assert installer.is_product_installed(package) is expected

    @pytest.mark.parametrize(
        "path,title,portal_type,review_state",
        [
            ("/", "Plone Site", "Plone Site", ""),
            ("/news", "News", "Folder", "published"),
            ("/events", "Events", "Folder", "published"),
        ],
    )
    def test_content_created(self, portal, path, title, portal_type, review_state):
        with api.env.adopt_roles(
            [
                "Manager",
            ]
        ):
            content = api.content.get(path=path)
        assert content.title == title
        assert content.portal_type == portal_type
        if review_state:
            assert api.content.get_state(content) == review_state
        else:
            with pytest.raises(WorkflowException) as exc:
                api.content.get_state(content)
            assert "No workflow provides" in str(exc)
