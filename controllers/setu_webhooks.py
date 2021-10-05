from datetime import datetime
from uuid import uuid4

from app.helpers import convertDateToISOFormat

from .user import updateConsentStatusAndConsentId

from schema.setu import Notifier_ConsentStatusNotification


def consentWebHookNotificationHandler(
    consentData: Notifier_ConsentStatusNotification,
):
    """Updates the consent Id and status"""
    updateConsentStatusAndConsentId(
        consentData.consentHandle, consentData.consentId, consentData.consentStatus
    )

    return _defaultWebHookResponse()


def _defaultWebHookResponse():
    """Returns a dict containing the response for the webhook"""
    return {
        "ver": "1.0",
        "timestamp": convertDateToISOFormat(datetime.now()),
        "txnid": str(uuid4()),
        "response": "OK",
    }
