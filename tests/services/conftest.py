import pytest


@pytest.fixture()
def app(functional):
    return functional["app"]


@pytest.fixture()
def portal(functional):
    return functional["portal"]


@pytest.fixture()
def http_request(functional):
    return functional["request"]
