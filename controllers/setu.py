"""Handles all the logic for Setu API (Consent, Data & Notification Flow)"""
from datetime import datetime
import requests
from uuid import uuid4

from utils.request_signing import makeDetachedJWS
from utils.setu_payloads import generateConsentObject

from app.config import api_keys
from app.helpers import parseControllerResponse


# CONSENT FLOW


def createAConsentRequestHandler(mobileNumber, **kwargs):
    """Sends an API request to the SETU Api requesting for a user's Consent
    Stores the ConsentHandle received from the API, and the status to the database"""

    isResponseParsed = kwargs.get("isParsed", False)
    (success, response) = _sendConsentRequestToSetu(mobileNumber)

    if not success:
        # request failed for some reason
        print(
            f"request consent request failed for {mobileNumber = } due to, {response}"
        )
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error=response
            )
            if isResponseParsed
            else {"error": response}
        )

    # successful, do something
    # TODO: do all db stuff
    return (
        parseControllerResponse(data={"setu": response}, statuscode=200)
        if isResponseParsed
        else True
    )


def _sendConsentRequestToSetu(phoneNumber):
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


def approveConsent(consentId):
    """Updates consent model with the relevent details"""
    pass


def rejectConsent(consentId):
    """Updates consent model with the relevent details"""
    pass


def revokeConsent(consentId):
    """Updates consent model with the relevent details"""
    pass


def pausedConsent(consentId):
    """Updates consent model with the relevent details"""
    pass
