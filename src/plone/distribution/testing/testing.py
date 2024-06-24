from .layer import PloneDistributionFixture
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.interfaces import PLONE_SITE_ID
from plone.testing.zope import WSGI_SERVER_FIXTURE


DISTRIBUTION = "testing"
ANSWERS = {
    "site_id": PLONE_SITE_ID,
    "title": "Testing Plone Site",
    "description": "A Plone Site",
    "site_logo": "name=teste;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",  # noQA
    "default_language": "en",
    "portal_timezone": "America/Sao_Paulo",
    "setup_content": True,
}


class BaseFixture(PloneDistributionFixture):
    PACKAGE_NAME: str = "plone.distribution.testing"
    SITES = ((DISTRIBUTION, ANSWERS),)


BASE_FIXTURE = BaseFixture()


class Layer(PloneSandboxLayer):
    defaultBases = (BASE_FIXTURE,)


FIXTURE = Layer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="DistributionLayer:IntegrationTesting",
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, WSGI_SERVER_FIXTURE),
    name="DistributionLayer:FunctionalTesting",
)
