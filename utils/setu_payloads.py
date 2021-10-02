from datetime import datetime

from app.helpers import convertDateToISOFormat


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
