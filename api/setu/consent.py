from datetime import datetime
import requests
from uuid import uuid4

from utils.helpers import convertDateToISOFormat
from utils.request_signing import makeDetachedJWS

from app.config import api_keys

# https://docs.setu.co/data/account-aggregator/consent-object#the-consent-object
def generateConsentObject(phoneNo):
    """Generates a consent flow object for the setu api"""

    consentObj = {
        "consentStart": convertDateToISOFormat(datetime.now()),
        # 1 day to accept the consent request
        "consentExpiry": convertDateToISOFormat(
            datetime.fromtimestamp((datetime.now().timestamp() + 60 * 60 * 24))
        ),
        "consentMode": "VIEW",
        "fetchType": "ONETIME",
        "consentTypes": ["TRANSACTIONS", "PROFILE", "SUMMARY"],
        "fiTypes": ["DEPOSIT", "BONDS", "INSURANCE_POLICIES", "PPF"],
        "DataConsumer": {"id": "FIU"},
        "Customer": {"id": f"{phoneNo}@setu-aa"},  # customer's data which we want
        "Purpose": {
            "code": "101",
            "refUri": "https://api.rebit.org.in/aa/purpose/101.xml",
            "text": "Wealth management service",
            "Category": {"type": "string"},
        },
        "FIDataRange": {  # all transactions in the past year
            "from": convertDateToISOFormat(
                datetime.fromtimestamp(
                    (datetime.now().timestamp() - (365 * 60 * 60 * 24))
                )
            ),
            "to": convertDateToISOFormat(datetime.now()),
        },
        "DataLife": {"unit": "MONTH", "value": 0},
        "Frequency": {"unit": "MONTH", "value": 3},
        "DataFilter": [{"type": "TRANSACTIONAMOUNT", "operator": ">=", "value": "10"}],
    }

    return consentObj


def sendFConsentRequest(phoneNumber):
    """Creates a consent request for the user with the given phone number and returns the response"""

    data = {
        "ver": "1.0",
        "timestamp": (datetime.now().isoformat()),
        "txnid": str(uuid4()),
        "ConsentDetail": generateConsentObject(phoneNumber),
    }
    headers = {
        "x-jws-signature": makeDetachedJWS(data),
        "client_api_key": api_keys.CLIENT_API_KEY,
    }

    url = "https://aa-sandbox.setu.co/Consent"

    response = requests.post(url, headers=headers, json=data)

    return response.status_code == requests.codes.ok, response.json()
