from flask import Blueprint, jsonify, request, session, redirect
from datetime import datetime

import requests
import time
import random

from rich import print

sk = Blueprint('sk', __name__, url_prefix='/sk')

sk_lives = [
    # "sk_live_0N3y0FZoNpBkyFNBFHNyXae400sPH5CJpK",
    "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",
    "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",
    "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",
]

# sk_lives = ["sk_live_TTegjpXgZPrYrmlFjjPJKiAr"]

stripe_auth = "https://api.stripe.com/v1/tokens"
stripe_payment = "https://api.stripe.com/v1/payment_methods"
stripe_intents = "https://api.stripe.com/v1/payment_intents"

cards_been_scanned = 0

def create_payment(ammount, ccn, exp_month, exp_year, cvc):
    auth = "Bearer " + random.choice(sk_lives)
    payment_method = requests.post(stripe_payment, 
        data={
            "type": "card",
            "card[number]": ccn,
            "card[exp_month]": exp_month,
            "card[exp_year]": exp_year,
            "card[cvc]": cvc,
            # "billing_details[line1]": "3rd Floor, 2nd Avenue",
            # "billing_details[line2]": "Near ABC Bank",
            # "billing_details[city]": "Brooklyn",
            # "billing_details[state]": "New York",
            # "billing_details[country]": "US",
            # "billing_details[postal_code]": "11231",
        },
        headers={
            "Authorization": auth,
            "content-type": "application/x-www-form-urlencoded"
        }
    )
    payment_method_body = payment_method.json()
    time.sleep(2)
    payment_intents = requests.post(stripe_intents, data={
        "amount": int(ammount),
        "currency": "usd",
        "payment_method": payment_method_body.get("id"),
        "description": "Arty",
        "confirm": True,
        "off_session": True,
    },
    headers={
        "Authorization": auth,
        "content-type": "application/x-www-form-urlencoded"
    })
    payment_intents_body = payment_intents.json()

    error = payment_intents_body.get("error", {})
    code = error.get("code", None)
    decline_code = error.get("decline_code", None)

    if error.get('type', None) == 'invalid_request_error':
        pass

    if error:
        print("Error aquired")
        return jsonify({"code": "declined"})

    if decline_code in ("generic_decline", "fraudulent"):
        print("Error")
        return jsonify({"code": "declined"})

    if not error:
        print("Success")
        return jsonify({"code": "success"})

    else:
        print(payment_intents_body)

@sk.route('/check', methods=['POST'])
def accses():
    accses = session['accses']
    expire = session['expires']

    if accses is None:
        return jsonify({'message': 'Invalid'})

    if datetime.strptime(expire, '%Y-%m-%d') < datetime.now():
        return jsonify({'message': 'Expired'})

    data = request.json

    if len(data) == 0:
        return jsonify({'message': 'Invalid'})

    ccn, exp_m, exp_y, cvc = data['ccn'], data['exp_m'], data['exp_y'], data['cvc']
    option = data['option']

    return create_payment(option, ccn, exp_m, exp_y, cvc)
    