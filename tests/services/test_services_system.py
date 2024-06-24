from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.distribution.api.distribution import SITE_REPORT_ANNO
from plone.restapi.testing import RelativeSession
from zope.annotation.interfaces import IAnnotations

import pytest


@pytest.fixture
def portal_uninstalled(portal):
    """Mock the uninstallation of a distribution."""
    import transaction

    annotations = IAnnotations(portal)
    report = annotations[SITE_REPORT_ANNO]
    current = report.name
    with transaction.manager:
        report.name = "mocked-dist"
        annotations[SITE_REPORT_ANNO] = report
    yield portal
    with transaction.manager:
        report.name = current
        annotations[SITE_REPORT_ANNO] = report


class TestServicesSystemGET:
    @pytest.fixture(autouse=True)
    def _api_session(self, portal):
        url = portal.absolute_url()
        api_session = RelativeSession(url)
        api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        api_session.headers.update({"Accept": "application/json"})
        self.api_session = api_session

    def test_system_get(self, portal):
        response = self.api_session.get("@system")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "plone.distribution" in data

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("distribution", "Testing Plone Site (testing)"),
        ],
    )
    def test_system_get_distribution(self, portal, attr, expected):
        response = self.api_session.get("@system")
        data = response.json()
        assert attr in data
        assert data[attr] == expected


class TestServicesSystemGETUninstalled:
    @pytest.fixture(autouse=True)
    def _api_session(self, portal_uninstalled):
        url = portal_uninstalled.absolute_url()
        api_session = RelativeSession(url)
        api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        api_session.headers.update({"Accept": "application/json"})
        self.api_session = api_session

    def test_system_get(self, portal_uninstalled):
        response = self.api_session.get("@system")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "plone.distribution" in data
        assert "distribution" in data
        assert data["distribution"] == "Uninstalled (mocked-dist)"
