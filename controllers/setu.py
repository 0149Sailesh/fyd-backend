"""Handles all the logic for Setu API (Consent, Data & Notification Flow)"""
from datetime import datetime
import requests
from uuid import uuid4
import json

from utils.request_signing import createAuthHeadersForAPI
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


def checkConsentStatusHandler(consentHandle, **kwargs):
    """Checks the consent status by pinging the SETU Api.
    Updates the database with relevent details"""
    isResponseParsed = kwargs.get("isParsed", False)

    success, response = _checkConsentStatusWithSetu(consentHandle)

    if not success:
        print(
            f"failed to check consent details for {consentHandle = } due to, {response}"
        )
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error=response
            )
            if isResponseParsed
            else {"error": response}
        )

    # TODO: do all db stuff
    # Store the consentId

    return (
        parseControllerResponse(data={"setu": response}, statuscode=200)
        if isResponseParsed
        else True
    )


def fetchSignedConsentHandler(consentId, **kwargs):
    """Fetched the signed consent from the setu API and sends appropriate response"""
    # Do we need to add something to the db ?
    isResponseParsed = kwargs.get("isParsed", False)

    success, response = _fetchSignedConsentFromSetu(consentId)

    if not success:
        print(
            f"failed to fetch signed consent details for {consentId = } due to, {response}"
        )
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error=response
            )
            if isResponseParsed
            else {"error": response}
        )

    # TODO: do all db stuff

    return (
        parseControllerResponse(data={"setu": response}, statuscode=200)
        if isResponseParsed
        else True
    )


def _fetchSignedConsentFromSetu(consentId):
    """Calls the SETU API to get a signed consent request by passing its unique id"""

    url = "https://aa-sandbox.setu.co/Consent/" + consentId
    headers = createAuthHeadersForAPI({"id": consentId})

    response = requests.get(url, headers=headers)
    print(json.dumps(response.json(), indent=2))

    return response.status_code == requests.codes.ok, response.json()


def _checkConsentStatusWithSetu(consentHandle):
    """Checks for consent status by hitting the setu api"""

    url = "https://aa-sandbox.setu.co/Consent/handle/" + consentHandle

    headers = createAuthHeadersForAPI({"id": consentHandle})

    response = requests.get(url, headers=headers)

    print(json.dumps(response.json(), indent=2))

    return response.status_code == requests.codes.ok, response.json()


def _sendConsentRequestToSetu(phoneNumber):
    """Creates a consent request for the user with the given phone number and returns the response"""

    data = {
        "ver": "1.0",
        "timestamp": (datetime.now().isoformat()),
        "txnid": str(uuid4()),
        "ConsentDetail": generateConsentObject(phoneNumber),
    }
    headers = createAuthHeadersForAPI(data)

    url = "https://aa-sandbox.setu.co/Consent"

    response = requests.post(url, headers=headers, json=data)

    print(json.dumps(response.json(), indent=2))

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
