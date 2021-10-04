"""Handles all the logic for Setu API (Consent, Data & Notification Flow)"""
from datetime import datetime
import requests
from uuid import uuid4
import json
import base64

from utils.request_signing import createAuthHeadersForSetuAPI
from utils.setu_payloads import (
    generateBodyForDataRequest,
    generateBodyForDecryptData,
    generateConsentObject,
)

from app.config import config
from app.helpers import convertDateToISOFormat, parseControllerResponse


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

    url = config.SETU_API_BASE_URL + "Consent/" + consentId
    headers = createAuthHeadersForSetuAPI({"id": consentId})

    response = requests.get(url, headers=headers)
    print(json.dumps(response.json(), indent=2))

    return response.status_code == requests.codes.ok, response.json()


def _checkConsentStatusWithSetu(consentHandle):
    """Checks for consent status by hitting the setu api"""

    url = config.SETU_API_BASE_URL + "Consent/handle/" + consentHandle

    headers = createAuthHeadersForSetuAPI({"id": consentHandle})

    response = requests.get(url, headers=headers)

    print(json.dumps(response.json(), indent=2))

    return response.status_code == requests.codes.ok, response.json()


def _sendConsentRequestToSetu(phoneNumber):
    """Creates a consent request for the user with the given phone number and returns the response"""

    data = {
        "ver": "1.0",
        "timestamp": convertDateToISOFormat(datetime.now()),
        "txnid": str(uuid4()),
        "ConsentDetail": generateConsentObject(phoneNumber),
    }
    headers = createAuthHeadersForSetuAPI(data)

    url = config.SETU_API_BASE_URL + "Consent"

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


# DATA FLOW


def requestFIDataHandler(**kwargs):
    """Requests for data by hitting the Setu API with the consentId and signedConsent"""

    (success, keys) = _generateNewECDHKeys()

    # TODO: store the keys in database

    isResponseParsed = kwargs.get("isParsed", False)

    if not success:
        # Something went wrong
        print("Couldn't generate keys because, " + keys)
        return (
            parseControllerResponse(data={"success": False}, statuscode=500, error=keys)
            if isResponseParsed
            else {"error": keys}
        )

    # TODO: Remove this hard code, fetch it from database
    signedConsent = ""
    consentId = ""

    (success, resp) = _sendDataReqestToSetu(signedConsent, consentId, keys)

    if not success:
        # Something went wrong
        print(f"Couldn't request data for {consentId = } because, {str(resp)}")
        return (
            parseControllerResponse(data={"success": False}, statuscode=500, error=resp)
            if isResponseParsed
            else {"error": resp}
        )

    return (
        parseControllerResponse(data={"setu": resp}, statuscode=200)
        if isResponseParsed
        else True
    )


def fetchFIDataHandler(**kwargs):
    """Gets the data from the Setu API after its ready, decrypts it and returns it as an array of data"""

    isResponseParsed = kwargs.get("isParsed", False)

    # TODO: remove hard coding and fetch this from database
    sessionId = ""
    (success, resp) = _fetchFIDataFromSetu(sessionId)

    if not success:
        # Something went wrong
        print(f"Couldn't fetch data for {sessionId = } due to {str(resp)}")
        return (
            parseControllerResponse(data={"success": False}, statuscode=500, error=resp)
            if isResponseParsed
            else {"error": resp}
        )

    # TODO: remove hard-code and fetch this from database
    ecdhKey = {}

    data, error = _decryptFIData(resp, ecdhKey)

    if error:
        print("Error decryption failed due to : " + str(error))
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error=error
            )
            if isResponseParsed
            else {"error": error}
        )

    return (
        parseControllerResponse(data={"setu": data}, statuscode=200)
        if isResponseParsed
        else True
    )


def _decryptFIData(encryptedData, ecdhKey):
    """Decrypts the data by sending it to the rahasya API and returns an array or decoded messages

    Args:
        encryptedData (dict): The FI Data which we get as a response to "/FI/Fetch" route in setu API api
        ecdhKey (dict): The Key generated by hitting the Rahasya API API

    Returns:
        Tuple(Response, Error): An array of decoded data, Error if any"""

    payloads = generateBodyForDecryptData(encryptedData, ecdhKey)

    url = config.RAHASYA_BASE_URL + "decrypt"

    decryptedData = []
    for payload in payloads:
        # print(json.dumps(payload, indent=4))
        resp = requests.post(url, json=payload)
        if resp.status_code != requests.codes.ok:
            return (None, resp.json())

        parsedData = resp.json()
        if parsedData["errorInfo"]:
            return (None, parsedData["errorInfo"])

        # base64 string -> bytes -> string -> json
        unencodedData = json.dumps(
            (base64.b64decode(parsedData["base64Data"])).decode("utf-8")
        )
        print(json.dumps(json.loads(unencodedData), indent=4))
        decryptedData.append(unencodedData)

    return decryptedData, None


def _generateNewECDHKeys():
    """Hits the Rahasya api to generate new keys needed for data transfer"""

    url = config.RAHASYA_BASE_URL + "generateKey"

    resp = requests.get(url)

    print(json.dumps(resp.json(), indent=2))

    return resp.status_code == requests.codes.ok, resp.json()


def _sendDataReqestToSetu(signedConsent, consentId, keys):
    """Sends Post req to Setu api along with signedConsent, consentId and public keys
    requesting for the user"s data"""
    payload = generateBodyForDataRequest(signedConsent, consentId, keys)

    print(json.dumps(payload, indent=4))

    headers = createAuthHeadersForSetuAPI(payload)

    url = config.SETU_API_BASE_URL + "FI/request"

    resp = requests.post(url, headers=headers, json=payload)

    return resp.status_code == requests.codes.ok, resp.json()


def _fetchFIDataFromSetu(sessionId):
    """Sends a get req to the SETU to get the FI data for the given sessionId"""

    url = config.SETU_API_BASE_URL + "FI/fetch/" + sessionId

    headers = createAuthHeadersForSetuAPI({"sessionId": sessionId})

    resp = requests.get(url, headers=headers)

    return resp.status_code == requests.codes.ok, resp.json()
