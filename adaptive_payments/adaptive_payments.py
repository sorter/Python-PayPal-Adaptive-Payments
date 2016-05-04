#!/usr/bin/env python
# adaptive-payments.py
# sy@sykhader.com

# python convenience functions for adaptive payments

import os
import json
import requests

home = os.path.expanduser("~")
PAYPAL_CREDENTIAL_FILE = "%s/.paypal-config.json" % home
print PAYPAL_CREDENTIAL_FILE
PAYPAL_CONFIG = json.loads(open(PAYPAL_CREDENTIAL_FILE).read())

ENDPOINT_URI = "AdaptivePayments/Pay"


def get_refresh_token(code):
    user = PAYPAL_CONFIG['clientid']
    passwd = PAYPAL_CONFIG['secret']
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = (('grant_type=authorization_code&response_type=token&redirect_uri='
            'urn:ietf:wg:oauth:2.0:oob&code=%s')
            % (code))
    r = requests.post('https://api.sandbox.paypal.com/v1/oauth2/token',
                    headers=headers, data=data,auth=(user,passwd))
    return r

def refresh_access_token(refresh):
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    user = PAYPAL_CONFIG['clientid']
    passwd = PAYPAL_CONFIG['secret']
    data = ('grant_type=refresh_token&refresh_token=%s' % refresh)
    url= 'https://api.sandbox.paypal.com/v1/identity/openidconnect/tokenservice'
    r = requests.post(url,headers=headers,data=data,auth=(user,passwd))
    return json.loads(r.content)["access_token"]


def user_id_payment(amt, receiver_id):
    """make payment, assumes paypal security credentials belong to the payer"""

    headers = {
        "X-PAYPAL-SECURITY-USERID": PAYPAL_CONFIG["api_username"], 
        "X-PAYPAL-SECURITY-PASSWORD": PAYPAL_CONFIG["api_password"],
        "X-PAYPAL-SECURITY-SIGNATURE": PAYPAL_CONFIG["api_signature"],
        "X-PAYPAL-REQUEST-DATA-FORMAT": "NV",
        "X-PAYPAL-RESPONSE-DATA-FORMAT": "NV" ,
        "X-PAYPAL-APPLICATION-ID": PAYPAL_CONFIG["app_id"]} 

    data= (("actionType=PAY&senderEmail=%s&cancelUrl=%s&currencyCode=USD&receiv"
            "erList.receiver(0).accountId=%s&receiverList.receiver(0).amount=%s&req"
            "uestEnvelope.errorLanguage=en_US&returnUrl=%s") 
            % (PAYPAL_CONFIG['sender_email'], PAYPAL_CONFIG['cancelUrl'], 
               receiver_id, amt, PAYPAL_CONFIG['returnUrl']))
    #url = PAYPAL_CONFIG['api_url'] + '/' + ENDPOINT_URI
    url = 'https://svcs.paypal.com/AdaptivePayments/' + ENDPOINT_URI
    r = requests.post(url, headers=headers, data=data)
    return r


def make_payment(amt, receiver_email):
    """make payment, assumes paypal security credentials belong to the payer"""

    headers = {
        "X-PAYPAL-SECURITY-USERID": PAYPAL_CONFIG["api_username"], 
        "X-PAYPAL-SECURITY-PASSWORD": PAYPAL_CONFIG["api_password"],
        "X-PAYPAL-SECURITY-SIGNATURE": PAYPAL_CONFIG["api_signature"],
        "X-PAYPAL-REQUEST-DATA-FORMAT": "NV",
        "X-PAYPAL-RESPONSE-DATA-FORMAT": "NV" ,
        "X-PAYPAL-APPLICATION-ID": PAYPAL_CONFIG["app_id"]} 

    data= (("actionType=PAY&senderEmail=%s&cancelUrl=%s&currencyCode=USD&receiv"
            "erList.receiver(0).email=%s&receiverList.receiver(0).amount=%s&req"
            "uestEnvelope.errorLanguage=en_US&returnUrl=%s") 
            % (PAYPAL_CONFIG['sender_email'], PAYPAL_CONFIG['cancelUrl'], 
               receiver_email, amt, PAYPAL_CONFIG['returnUrl']))
    url = PAYPAL_CONFIG['api_url'] + '/' + ENDPOINT_URI
    r = requests.post(url, headers=headers, data=data)

u = 'https://api.sandbox.payypal.com/v1/identiy/openidconnect/userinfo/?schema=openid'
access_token = 'A015MPrEAeZL6c9hxHK-9zQV3lJj1fP0MMXADcHQ6tpsKjY'


def get_user_id(access_token):
    u = ('https://api.sandbox.paypal.com/v1/identity/openidconnect/userinfo/'
             '?schema=openid')
    headers = { 'Content-Type': 'application/json', 
                'Authorization': 'Bearer %s' % access_token}

    r = requests.get(u,headers=headers)
    return json.loads(r.content)["user_id"]
