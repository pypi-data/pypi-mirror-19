class DummyStripeUtility(object):
    def get_stripe_api(self):
        return DummyStripe()
 
class DummyStripe(object):
    api_key = '123456789'

    @property
    def Event(self):
        return DummyEvents()


class DummyEvents(object):
    def __init__(self):
        self.dummy_event = {
            "id": "test_passing",
            "created": 123456789,
            "livemode": False,
            "type": "charge.succeeded",
            "data": {
                "object": {
                    "id": "ch_2OmwsdSNjmFvGQ",
                    "object": "charge",
                    "created": 1376706172,
                    "livemode": False,
                    "paid": True,
                    "amount": 500,
                    "currency": "usd",
                    "refunded": False,
                    "card": {
                        "id": "card_2OmwN1y86pCJy2",
                        "object": "card",
                        "last4": "4242",
                        "type": "Visa",
                        "exp_month": 1,
                        "exp_year": 2050,
                        "fingerprint": "qhjxpr7DiCdFYTlH",
                        "customer": None,
                        "country": "US",
                        "name": None,
                        "address_line1": None,
                        "address_line2": None,
                        "address_city": None,
                        "address_state": None,
                        "address_zip": None,
                        "address_country": None,
                        "cvc_check": "pass",
                        "address_line1_check": None,
                        "address_zip_check": None
                    },
                    "captured": True,
                    "refunds": [
                    ],
                    "balance_transaction": "txn_2OmwHoZeThcMdu",
                    "failure_message": None,
                    "failure_code": None,
                    "amount_refunded": 0,
                    "customer": None,
                    "invoice": None,
                    "description": None,
                    "dispute": None,
                }
            },
            "object": "event",
            "pending_webhooks": 0,
            "request": "iar_2Omw24HYWicSuq"
        } 

    def retrieve(self, id):
        self.dummy_event['id'] = id
        if id == 'test_failing_id':
            self.dummy_event['id'] = 'test_id_failing'
        if id == 'test_failing_type':
            self.dummy_event['type'] = 'failing'
        if id == 'test_failing_created':
            self.dummy_event['created'] = 0 
        return self.dummy_event
