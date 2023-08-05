from five import grok

from z3c.form import interfaces

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import Interface

from plone.app.registry.browser import controlpanel

MODE_VOCABULARY = SimpleVocabulary((
    SimpleTerm(value="live", title=u"Live (Production Mode)"),
    SimpleTerm(value="test", title=u"Test (Test Mode, no transactions really go through, be careful)"),
))
class StripeModesVocabulary(object):
    grok.implements(IVocabularyFactory)
    def __call__(self, context):
        return MODE_VOCABULARY
grok.global_utility(StripeModesVocabulary, name=u"collective.stripe.modes")

CURRENCY_VOCABULARY = SimpleVocabulary((
    SimpleTerm(value="usd", title=u"USD - $"),
))

class IStripeSettings(Interface):
    """ Global settings for collective.stripe stored in the registry """
    mode = schema.Choice(
        title=u"Mode",
        description=u"Determines whether calls to the Stripe API are made using the Test or the Live key",
        vocabulary=MODE_VOCABULARY,
        default=u"test",
    )
    test_secret_key = schema.TextLine(
        title=u"Test Secret Key",
        description=u"Located under Account Settings -> API Keys when logged into stripe.com",
    )
    test_publishable_key = schema.TextLine(
        title=u"Test Publishable Key",
        description=u"Located under Account Settings -> API Keys when logged into stripe.com",
    )
    live_secret_key = schema.TextLine(
        title=u"Live Secret Key",
        description=u"Located under Account Settings -> API Keys when logged into stripe.com",
    )
    live_publishable_key = schema.TextLine(
        title=u"Live Publishable Key",
        description=u"Located under Account Settings -> API Keys when logged into stripe.com",
    )
    currency = schema.Choice(
        title=u"Currency",
        description=u"The currency, used in calls to the Stripe API",
        vocabulary=CURRENCY_VOCABULARY,
        default=u"usd",
    )

class StripeSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IStripeSettings
    label = u"Stripe Settings"
    description = u"Configuration for collective.stripe providing integration with Stripe for payment processing"

    def updateFields(self):
        super(StripeSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(StripeSettingsEditForm, self).updateWidgets()

class StripeSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = StripeSettingsEditForm
