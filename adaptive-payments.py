#!/usr/bin/env python
# adaptive-payments.py
# sy@sykhader.com

# python convenience functions for adaptive payments

import os
import json
import requests

abs_script_dir_path = os.path.dirname(os.path.abspath(__file__))
PAYPAL_CREDENTIAL_FILE = "%s/paypal_config.json" % abs_script_dir_path
PAYPAL_CONFIG = json.loads(PAYPAL_CREDENTIAL_FILE)

ENDPOINT_URI = "AdaptivePayments/Pay"

headers = {
    "X-PAYPAL-SECURITY-USERID": PAYPAL_CONFIG["api_username"], 
    "X-PAYPAL-SECURITY-PASSWORD": PAYPAL_CONFIG["api_password"],
    "X-PAYPAL-SECURITY-SIGNATURE": PAYPAL_CONFIG["api_signature"],
    "X-PAYPAL-REQUEST-DATA-FORMAT": "NV",
    "X-PAYPAL-RESPONSE-DATA-FORMAT": "NV" ,
    "X-PAYPAL-APPLICATION-ID": PAYPAL_CONFIG["app_id"]} 

def make_payment(self, amt, receiver_email):
    """make payment, assumes paypal security credentials belong to the payer"""

    #payload = {
    #  "actionType":"PAY",
    #  "currencyCode":"USD",
    #  "receiverList":{
    #    "receiver":[{
    #      "amount":str(amt),
    #      "email": receiver_email
    #    }]
    #  },
    #  "returnUrl":PAYPAL_CONFIG['returnUrl'], 
    #  "cancelUrl":PAYPAL_CONFIG['cancelUrl'],
    #  "requestEnvelope":{
    #  "errorLanguage":"en_US",
    #  "detailLevel":"ReturnAll"
    #  }
    #}
    data= (("actionType=PAY&senderEmail=%s&cancelUrl=%s&currencyCode=USD&receiv"
            "erList.receiver(0).email=%s&receiverList.receiver(0).amount=%s&req"
            "uestEnvelope.errorLanguage=en_US&returnUrl=%s") 
            % (PAYPAL_CONFIG['sender_email'], PAYPAL_CONFIG['cancelUrl'], 
               receiver_email, amt, PAYPAL_CONFIG['returnUrl']))
    url = PAYPAL_CONFIG['api_url'] + '/' + ENDPOINT_URI
    r = requests.post(url, headers=headers, data=data)
