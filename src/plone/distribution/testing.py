from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import plone.distribution


class DistributionLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.volto

        self.loadZCML(package=plone.distribution)
        self.loadZCML(package=plone.volto)


FIXTURE = DistributionLayer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="DistributionLayer:IntegrationTesting",
)
