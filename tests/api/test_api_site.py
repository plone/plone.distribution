from plone import api
from plone.distribution.api import distribution as dist_api
from plone.distribution.api import site as site_api
from Products.CMFPlone.Portal import PloneSite

import pytest


@pytest.fixture
def answers() -> dict:
    """Answers payload for new site creation."""
    return {
        "site_id": "PloneBrasil",
        "title": "Plone site in Brazil",
        "description": "A simple Plone Site",
        "default_language": "pt-br",
        "portal_timezone": "America/Sao_Paulo",
        "setup_content": False,  # Avoid committing a transaction
    }


@pytest.fixture
def site(app, answers) -> PloneSite:
    """Create a new Plone site via a distribution."""
    site_id = answers["site_id"]
    distribution_name = "testing"
    yield site_api.create(app, distribution_name, answers)
    app.manage_delObjects([site_id])


class TestApiSite:
    def test_get_sites(self, app, integration):
        sites = site_api.get_sites(app)
        # Integration test creates a Plone Site
        assert len(sites) == 1
        site = sites[0]
        assert isinstance(site, PloneSite)

    @pytest.mark.parametrize(
        "distribution_name",
        [
            "testing",
        ],
    )
    def test_create(self, app, integration, answers, distribution_name):
        sites = site_api.get_sites(app)
        total_sites = len(sites)
        with api.env.adopt_roles(["Manager"]):
            answers["site_id"] = f"{distribution_name}_01"
            new_site = site_api.create(app, distribution_name, answers)
        sites = site_api.get_sites(app)
        assert len(sites) == total_sites + 1
        site = sites[-1]
        assert isinstance(site, PloneSite)
        assert site.title == new_site.title

    def test_get_creation_report_new_site(self, site):
        from datetime import datetime
        from plone.distribution.core import SiteCreationReport

        report = dist_api.get_creation_report(site)
        assert isinstance(report, SiteCreationReport)
        assert report.name == "testing"
        assert isinstance(report.date, datetime)
        assert isinstance(report.answers, dict)
        assert report.answers["title"] == site.title
