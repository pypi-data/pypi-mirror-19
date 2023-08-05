from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import ploneSite
from plone.app.testing import quickInstallProduct
import transaction


class CollectiveStripeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.stripe
        self.loadZCML(package=collective.stripe)

        z2.installProduct(app, 'collective.stripe')

    def setUpPloneSite(self, portal):
        quickInstallProduct(portal, 'collective.stripe')
        self.applyProfile(portal, 'collective.stripe:default')
        transaction.commit()

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'collective.stripe')


FIXTURE = CollectiveStripeLayer()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name='collective.stripe:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name='collective.stripe:Functional')
