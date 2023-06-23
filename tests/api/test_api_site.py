from plone import api
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
    distribution_name = "default"
    return site_api.create(app, distribution_name, answers)


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
    def test_create(self, app, integration, answers, distribution_name):
        with api.env.adopt_roles(["Manager"]):
            new_site = site_api.create(app, distribution_name, answers)
        sites = site_api.get_sites(app)
        assert len(sites) == 4
        site = sites[-1]
        assert isinstance(site, PloneSite)
        assert site.title == new_site.title

    def test_get_creation_report_old_site(self, app, integration):
        # An existing site (or older distribution will not have a report)
        report = site_api.get_creation_report(app.Plone)
        assert report is None

    def test_get_creation_report_new_site(self, site):
        from datetime import datetime
        from plone.distribution.core import SiteCreationReport

        report = site_api.get_creation_report(site)
        assert isinstance(report, SiteCreationReport)
        assert report.name == "default"
        assert isinstance(report.date, datetime)
        assert isinstance(report.answers, dict)
        assert report.answers["title"] == site.title
