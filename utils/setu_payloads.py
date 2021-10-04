from datetime import datetime
from uuid import uuid4

from app.helpers import convertDateToISOFormat


# https://docs.setu.co/data/account-aggregator/consent-object#the-consent-object
def generateConsentObject(phoneNo):
    """Generates a consent flow object for the setu api"""

    consentObj = {
        "consentStart": convertDateToISOFormat(datetime.now()),
        # 1 day to accept the consent request
        "consentExpiry": convertDateToISOFormat(
            datetime.fromtimestamp((datetime.now().timestamp() + 24 * 60 * 60))
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
        "FIDataRange": {  # all transactions in the past year + 12 hrs
            "from": convertDateToISOFormat(
                datetime.fromtimestamp(
                    (datetime.now().timestamp() - ((365 * 24 * 60 * 60) + (12 * 3600)))
                )
            ),
            "to": convertDateToISOFormat(datetime.now()),
        },
        "DataLife": {"unit": "MONTH", "value": 0},
        "Frequency": {"unit": "MONTH", "value": 3},
        "DataFilter": [{"type": "TRANSACTIONAMOUNT", "operator": ">=", "value": "10"}],
    }

    return consentObj


def generateBodyForDataRequest(signedConsent, consentId, keys):
    """Generates the body for requesting FI data"""
    return {
        "ver": "1.0",
        "timestamp": convertDateToISOFormat(datetime.now()),
        "txnid": str(uuid4()),
        "FIDataRange": {  # all transactions in the past year
            "from": convertDateToISOFormat(
                datetime.fromtimestamp(
                    (datetime.now().timestamp() - ((365 * 24 * 60 * 60)))
                )
            ),
            "to": convertDateToISOFormat(datetime.now()),
        },
        "Consent": {"id": consentId, "digitalSignature": signedConsent.split(".")[2]},
        "KeyMaterial": keys["KeyMaterial"],
    }
