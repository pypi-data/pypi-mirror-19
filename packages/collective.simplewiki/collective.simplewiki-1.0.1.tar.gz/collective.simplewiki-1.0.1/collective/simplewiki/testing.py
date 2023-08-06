from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2
from Products.CMFCore.utils import getToolByName
from zope.configuration import xmlconfig


class CollectiveSimpleWikiLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.simplewiki
        xmlconfig.file(
            'configure.zcml',
            collective.simplewiki,
            context=configurationContext
        )
        z2.installProduct(app, 'collective.simplewiki')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'collective.simplewiki')

    def setUpPloneSite(self, portal):
        super(CollectiveSimpleWikiLayer, self).setUpPloneSite(portal)
        # install into the Plone site
        applyProfile(portal, 'plone.app.registry:default')
        applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'collective.simplewiki:default')
        setRoles(portal, TEST_USER_ID, ('Member', 'Manager'))
        workflowTool = getToolByName(portal, 'portal_workflow')
        workflowTool.setDefaultChain('plone_workflow')


COLLECTIVE_SIMPLEWIKI_FIXTURE = CollectiveSimpleWikiLayer()

COLLECTIVE_SIMPLEWIKI_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_SIMPLEWIKI_FIXTURE,),
    name="CollectiveSimpleWikiLayer:Integration"
)
