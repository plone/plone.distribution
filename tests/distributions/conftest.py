import pytest


@pytest.fixture()
def app(functional):
    return functional["app"]


@pytest.fixture()
def portal_default(functional):
    return functional["portal"]


@pytest.fixture()
def portal_classic(app):
    return app["classic"]


@pytest.fixture()
def http_request(functional):
    return functional["request"]
