from datetime import datetime
from uuid import uuid4

from app.helpers import convertDateToISOFormat

from schema.setu import ConsentNotificationWebhook_Request
from .setu import (
    approveConsent,
    pausedConsent,
    rejectConsent,
    revokeConsent,
    pausedConsent,
)


def consentWebHookNotificationHandler(
    consentData: ConsentNotificationWebhook_Request.ConsentStatusNotification,
):
    """Handler for consent webhook"""
    consentStatusHandler = {
        "ACTIVE": approveConsent,
        "REJECTED": rejectConsent,
        "REVOKED": revokeConsent,
        "PAUSED": pausedConsent,
    }

    # TODO: Finish this route
    (consentStatusHandler[consentData.consentStatus])(consentData.consentId)

    return _defaultWebHookResponse()


def _defaultWebHookResponse():
    """Returns a dict containing the response for the webhook"""
    return {
        "ver": "1.0",
        "timestamp": convertDateToISOFormat(datetime.now()),
        "txnid": str(uuid4()),
        "response": "OK",
    }
