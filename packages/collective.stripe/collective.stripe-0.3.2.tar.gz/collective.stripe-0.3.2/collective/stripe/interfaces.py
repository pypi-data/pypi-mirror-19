from zope.interface import Interface

class IStripeModeChooser(Interface):
    """ Interface for content types which can control 
        the Stripe mode, overriding the global control 
        panel setting 
    """

    def get_stripe_mode():
        """ Returns either 'live' or 'test' """

class IStripeEnabledView(Interface):
    """ Interface for views using Stripe """

    def show_stripe():
        """ Returns boolean for whether or not to include the stripe javascript """


# Webhook triggered events

class BaseWebhookEvent(object):
    def __init__(self, data):
        self.data = data
# Account events

class IAccountUpdatedEvent(BaseWebhookEvent):
    """ describes an account - Occurs whenever an account status or property has changed. """

class IAccountApplicationDeauthorizedEvent(BaseWebhookEvent):
    """ describes an application - Occurs whenever a user deauthorizes an application. Sent to the related application only. """

# Balance events

class IBalanceAvailableEvent(BaseWebhookEvent):
    """ describes a balance - Occurs whenever your Stripe balance has been updated (e.g. when a charge collected is available to be paid out). By default, Stripe will automatically transfer any funds in your balance to your bank account on a daily basis. """

# Charge events

class IChargeSucceededEvent(BaseWebhookEvent):
    """ describes a charge - Occurs whenever a new charge is created and is successful. """

class IChargeFailedEvent(BaseWebhookEvent):
    """ describes a charge - Occurs whenever a failed charge attempt occurs. """

class IChargeRefundedEvent(BaseWebhookEvent):
    """ describes a charge - Occurs whenever a charge is refunded, including partial refunds. """

class IChargeCapturedEvent(BaseWebhookEvent):
    """ describes a charge - Occurs whenever a previously uncaptured charge is captured. """

class IChargeDisputeCreatedEvent(BaseWebhookEvent):
    """ describes a dispute - Occurs whenever a customer disputes a charge with their bank (chargeback). """

class IChargeDisputeUpdatedEvent(BaseWebhookEvent):
    """ describes a dispute - Occurs when the dispute is updated (usually with evidence). """

class IChargeDisputeClosedEvent(BaseWebhookEvent):    """ describes a dispute - Occurs when the dispute is resolved and the dispute status changes to won or lost. """# Customer events

class ICustomerCreatedEvent(BaseWebhookEvent):
    """ describes a customer - Occurs whenever a new customer is created. """

class ICustomerUpdatedEvent(BaseWebhookEvent):
    """ describes a customer - Occurs whenever any property of a customer changes. """

class ICustomerDeletedEvent(BaseWebhookEvent):
    """ describes a customer - Occurs whenever a customer is deleted. """

class ICustomerCardCreatedEvent(BaseWebhookEvent):
    """ describes a card - Occurs whenever a new card is created for the customer. """

class ICustomerCardUpdatedEvent(BaseWebhookEvent):
    """ describes a card - Occurs whenever a card's details are changed. """

class ICustomerCardDeletedEvent(BaseWebhookEvent):
    """ describes a card - Occurs whenever a card is removed from a customer. """

class ICustomerSubscriptionCreatedEvent(BaseWebhookEvent):
    """ describes a subscription - Occurs whenever a customer with no subscription is signed up for a plan. """

class ICustomerSubscriptionCreatedEvent(BaseWebhookEvent):
    """ describes a subscription - Occurs whenever a customer with no subscription is signed up for a plan. """

class ICustomerSubscriptionUpdatedEvent(BaseWebhookEvent):
    """ describes a subscription - Occurs whenever a subscription changes. Examples would include switching from one plan to another, or switching status from trial to active. """

class ICustomerSubscriptionDeletedEvent(BaseWebhookEvent):
    """ describes a subscription - Occurs whenever a customer ends their subscription. """

class ICustomerSubscriptionTrialWillEndEvent(BaseWebhookEvent):
    """ describes a subscription - Occurs three days before the trial period of a subscription is scheduled to end. """

class ICustomerDiscountCreatedEvent(BaseWebhookEvent):
    """ describes a discount - Occurs whenever a coupon is attached to a customer. """

class ICustomerDiscountUpdatedEvent(BaseWebhookEvent):
    """ describes a discount - Occurs whenever a customer is switched from one coupon to another. """

class ICustomerDiscountDeletedEvent(BaseWebhookEvent):
    """ describes a discount - Occurs whenever a customer's discount is removed. """

# Invoice events

class IInvoiceCreatedEvent(BaseWebhookEvent):
    """ describes an invoice - Occurs whenever a new invoice is created. If you are using webhooks, Stripe will wait one hour after they have all succeeded to attempt to pay the invoice; the only exception here is on the first invoice, which gets created and paid immediately when you subscribe a customer to a plan. If your webhooks do not all respond successfully, Stripe will continue retrying the webhooks every hour and will not attempt to pay the invoice. After 3 days, Stripe will attempt to pay the invoice regardless of whether or not your webhooks have succeeded. See how to respond to a webhook. """

class IInvoiceUpdatedEvent(BaseWebhookEvent):
    """ describes an invoice - Occurs whenever an invoice changes (for example, the amount could change). """

class IInvoicePaymentSucceededEvent(BaseWebhookEvent):
    """ describes an invoice - Occurs whenever an invoice attempts to be paid, and the payment succeeds. """

class IInvoicePaymentFailedEvent(BaseWebhookEvent):
    """ describes an invoice - Occurs whenever an invoice attempts to be paid, and the payment fails. """

class IInvoiceItemCreatedEvent(BaseWebhookEvent):
    """ describes an invoice item - Occurs whenever an invoice item is created. """

class IInvoiceItemUpdatedEvent(BaseWebhookEvent):
    """ describes an invoice item - Occurs whenever an invoice item is updated. """

class IInvoiceItemDeletedEvent(BaseWebhookEvent):
    """ describes an invoice item - Occurs whenever an invoice item is deleted. """

# Plan events

class IPlanCreatedEvent(BaseWebhookEvent):
    """ describes a plan - Occurs whenever a plan is created. """

class IPlanUpdatedEvent(BaseWebhookEvent):
    """ describes a plan - Occurs whenever a plan is updated. """

class IPlanDeletedEvent(BaseWebhookEvent):
    """ describes a plan - Occurs whenever a plan is deleted. """

# Coupon related events

class ICouponCreatedEvent(BaseWebhookEvent):
    """ describes a coupon - Occurs whenever a coupon is created. """

class ICouponDeletedEvent(BaseWebhookEvent):
    """ describes a coupon - Occurs whenever a coupon is deleted. """

# Transfer events

class ITransferCreatedEvent(BaseWebhookEvent):
    """ describes a transfer - Occurs whenever a new transfer is created. """

class ITransferUpdatedEvent(BaseWebhookEvent):
    """ describes a transfer - Occurs whenever the amount of a pending transfer is updated. """

class ITransferPaidEvent(BaseWebhookEvent):
    """ describes a transfer - Occurs whenever a sent transfer is expected to be available in the destination bank account. If the transfer failed, a transfer.failed webhook will additionally be sent at a later time. """

class ITransferFailedEvent(BaseWebhookEvent):
    """ describes a transfer - Occurs whenever Stripe attempts to send a transfer and that transfer fails. """

# Ping event

class IPingEvent(BaseWebhookEvent):
    """ has no description - May be sent by Stripe at any time to see if a provided webhook URL is working. """
