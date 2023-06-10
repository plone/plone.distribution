from plone import api
from plone.distribution.api import site as site_api
from Products.CMFPlone.Portal import PloneSite

import pytest


class TestApiSite:
    def test_get_sites(self, app, integration):
        sites = site_api.get_sites(app)
        # Integration test creates a Plone Site
        assert len(sites) == 3
        site = sites[0]
        assert isinstance(site, PloneSite)

    @pytest.mark.parametrize(
        "distribution_name",
        [
            "default",
            "classic",
        ],
    )
    def test_create(self, app, integration, distribution_name):
        with api.env.adopt_roles(["Manager"]):
            answers = {
                "site_id": "PloneBrasil",
                "title": "Plone site in Brazil",
                "description": "A simple Plone Site",
                "default_language": "pt-br",
                "portal_timezone": "America/Sao_Paulo",
                "setup_content": False,  # Avoid committing a transaction
            }
            new_site = site_api.create(app, distribution_name, answers)
        sites = site_api.get_sites(app)
        assert len(sites) == 4
        site = sites[-1]
        assert isinstance(site, PloneSite)
        assert site.title == new_site.title
