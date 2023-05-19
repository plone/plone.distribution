from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession

import pytest


class TestServicesSite:
    @pytest.fixture(autouse=True)
    def _api_session(self, app):
        url = app.absolute_url()
        api_session = RelativeSession(url)
        api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        api_session.headers.update({"Accept": "application/json"})
        self.api_session = api_session


class TestServicesSitesGET(TestServicesSite):
    def test_sites_get_anonymous(self, app):
        self.api_session.auth = None
        response = self.api_session.get("@sites")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["can_manage"] is False

    def test_sites_get_authenticated(self, app):
        response = self.api_session.get("@sites")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["can_manage"] is True

    def test_sites_get_distributions(self, app):
        response = self.api_session.get("@sites")
        data = response.json()
        distributions = data["distributions"]
        assert isinstance(distributions, list)
        assert len(distributions) == 2
        assert distributions[0]["name"] == "default"
        assert distributions[0]["title"] == "Plone Site"

    def test_sites_get_sites(self, app):
        response = self.api_session.get("@sites")
        data = response.json()
        sites = data["sites"]
        assert isinstance(sites, list)
        assert len(sites) == 3
        assert sites[0]["id"] == "plone"
        assert sites[0]["needs_upgrade"] is False


class TestServicesSitesPOST(TestServicesSite):
    @pytest.fixture(autouse=True)
    def _answers(self):
        self.answers = {
            "site_id": "PloneBrasil",
            "title": "Plone site in Brazil",
            "description": "A simple Plone Site",
            "default_language": "pt-br",
            "portal_timezone": "America/Sao_Paulo",
            "setup_content": True,
        }

    @pytest.mark.parametrize(
        "distribution_name",
        [
            "default",
            "classic",
        ],
    )
    def test_sites_create_success(self, app, distribution_name):
        response = self.api_session.post(
            f"@sites/{distribution_name}", json=self.answers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "PloneBrasil"
        assert data["@type"] == "Plone Site"

    @pytest.mark.parametrize(
        "distribution_name",
        [
            "someStrangeName",
            "404",
        ],
    )
    def test_sites_create_failure(self, app, distribution_name):
        """Test POST with non-existing distribution names."""
        response = self.api_session.post(
            f"@sites/{distribution_name}", json=self.answers
        )
        assert response.status_code == 404
        data = response.json()
        assert data["message"].startswith("Resource not found:")
