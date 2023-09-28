from decimal import Decimal
from typing import Dict
import stripe
from django.conf import settings
FRONTEND_SUBSCRIPTION_SUCCESS_URL = settings.SUBSCRIPTION_SUCCESS_URL
FRONTEND_SUBSCRIPTION_CANCEL_URL = settings.SUBSCRIPTION_FAILED_URL
stripe.api_key = settings.STRIPE_SECRET_KEY

# NOTE: these methods are stripe wrappers to avoid repeat stripe calls.
# They should not contains (or at least a few) business logic.
# That's why it's OK to NOT test them, as it would lead to testing stripe itself.
# However, the methods that calls these methods should be tested extensively.

###### Moje trenutno potrebne metode #########
def create_stripe_product(name):
    return stripe.Product.create(name=name)


def create_stripe_price(price, product):
    return stripe.Price.create(
        unit_amount=price,
        currency="usd",
        product=product.id
    )


def create_stripe_customer_id(email):
    return stripe.Customer.create(email=email)


def create_stripe_subscription(client, program):
    return stripe.Subscription.create(
            customer=client.stripe_customer_id,
            items=[{'price': program.price_id_stripe}],  # Assuming you have a Stripe Price ID for the program
            cancel_url=FRONTEND_SUBSCRIPTION_CANCEL_URL,  # Get the cancellation URL from settings
            success_url=FRONTEND_SUBSCRIPTION_SUCCESS_URL,  # Get the success URL from settings
    )


def create_stripe_payment_method(token):
    return stripe.PaymentMethod.create(
        type='card',
        card={
            'token': token,  # Use the token ID here
        },
    )


def attach_stripe_payment_method(payment_method_id, customer_id):
    return stripe.PaymentMethod.attach(
        payment_method_id,
        customer=customer_id,
    )


def list_stripe_payment_methods(customer_id):
    return stripe.PaymentMethod.list(
        customer=customer_id,
        # list by payment method type
        type='card'
    )


def set_default_stripe_payment_method(customer_id, payment_method_id):
    return stripe.Customer.modify(
        customer_id,
        invoice_settings={'default_payment_method': payment_method_id}
    )









# Customer

def retrieve_stripe_customer(stripe_id):
    return stripe.Customer.retrieve(stripe_id)


# Setup Intent


def retrieve_stripe_setup_intent(intent_id):
    return stripe.SetupIntent.retrieve(intent_id)


def create_stripe_setup_intent():
    # customer is not provided in arguments, because it may not exist at this time
    return stripe.SetupIntent.create()


# Payment Intent


def retrieve_stripe_payment_intent(intent_id):
    return stripe.PaymentIntent.retrieve(intent_id)


# def create_stripe_payment_intent(
#     stripe_id: str,
#     receipt_email: str,
#     amount: Decimal,
#     capture_method: str,
#     payment_method=None,
#     description=None,
#     save_card=False,
# ):
#     """https://stripe.com/docs/api/payment_intents/create
#     This simple wrapper allow to abstract some attributes that should always stay the same
#     (eg. confirmation_method)
#     """

#     kwargs = dict(
#         amount=euros_to_cents(amount),
#         capture_method=capture_method,
#         currency="eur",
#         customer=stripe_id,
#         confirmation_method="automatic",
#         payment_method=payment_method,
#         receipt_email=receipt_email,
#         description=description,
#     )
#     if save_card:
#         kwargs["setup_future_usage"] = "off_session"
#     return stripe.PaymentIntent.create(**kwargs)


def capture_stripe_payment_intent(payment_intent_id):
    return stripe.PaymentIntent.capture(payment_intent_id)


def cancel_stripe_payment_intent(payment_intent_id):
    return stripe.PaymentIntent.cancel(payment_intent_id)


# Payment Method


def get_stripe_cards(stripe_id):
    return stripe.PaymentMethod.list(customer=stripe_id, type="card")


def retrieve_payment_method(payment_method):
    return stripe.PaymentMethod.retrieve(payment_method)


def detach_stripe_cards(cards: Dict) -> None:
    for card_to_detach in cards:
        detach_stripe_card_from_id(card_to_detach["id"])


def detach_stripe_card_from_id(card_id: int) -> None:
    stripe.PaymentMethod.detach(card_id)


def attach_stripe_card(stripe_id, payment_method):
    return stripe.PaymentMethod.attach(payment_method, customer=stripe_id)


def add_or_replace_stripe_card(stripe_id, setup_intent_id):
    """
    Try to add a new card to an existing stripe account
    If it succeeds, removes all other payment methods. Returns the new one.
    """
    customer_cards_before_adding_new_one = get_stripe_cards(stripe_id)
    new_card = attach_stripe_card(
        stripe_id, payment_method=retrieve_stripe_setup_intent(setup_intent_id)["payment_method"]
    )
    detach_stripe_cards(customer_cards_before_adding_new_one)  # normally 1 card only max

    return new_card


def get_stripe_card_infos(stripe_id):
    # NOTE: we should prevent to have more than one card recorded to avoid weird behaviour
    customer_cards = get_stripe_cards(stripe_id)
    return customer_cards["data"][0]["card"] if customer_cards["data"] else dict()


def delete_all_stripe_cards(stripe_id) -> None:
    customer_cards = get_stripe_cards(stripe_id)
    detach_stripe_cards(customer_cards)  # normally 1 card only max


# Charges


def get_stripe_receipt_from_charge_id(stripe_id, charge_id):
    charge = stripe.Charge.retrieve(charge_id)
    assert charge.customer == stripe_id  # security
    return charge.receipt_url
