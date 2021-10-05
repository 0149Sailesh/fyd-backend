"""Handles all the logic for Setu API (Consent, Data & Notification Flow)"""
from datetime import datetime
import requests
from uuid import uuid4
import json
import base64
from controllers.user import createFIConsentObj

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
    # TODO: refactor so its like other
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
            else False,
            {"error": response},
        )

    return (
        parseControllerResponse(data={"setu": response}, statuscode=200)
        if isResponseParsed
        else (response, None)
    )


def checkConsentStatusHandler(consentHandle, **kwargs):
    """Checks the consent status by pinging the SETU Api.
    Updates the database with relevent details"""
    isResponseParsed = kwargs.get("isParsed", False)

    response, error = _checkConsentStatusWithSetu(consentHandle)

    if error:
        print(f"failed to check consent details for {consentHandle = } due to, {error}")
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error=error
            )
            if isResponseParsed
            else None,
            {"error": error},
        )

    return (
        parseControllerResponse(data={"setu": response}, statuscode=200)
        if isResponseParsed
        else response,
        None,
    )


def fetchSignedConsentHandler(consentId, **kwargs):
    """Fetched the signed consent from the setu API and sends appropriate response"""
    # Do we need to add something to the db ?
    isResponseParsed = kwargs.get("isParsed", False)

    response, error = _fetchSignedConsentFromSetu(consentId)

    if error:
        print(
            f"failed to fetch signed consent details for {consentId = } due to, {error}"
        )
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error=error
            )
            if isResponseParsed
            else None,
            {"error": error},
        )

    # TODO: do all db stuff

    return (
        parseControllerResponse(data={"setu": response}, statuscode=200)
        if isResponseParsed
        else (response, None)
    )


def _fetchSignedConsentFromSetu(consentId):
    """Calls the SETU API to get a signed consent request by passing its unique id"""

    url = config.SETU_API_BASE_URL + "Consent/" + consentId
    headers = createAuthHeadersForSetuAPI({"id": consentId})

    response = requests.get(url, headers=headers)
    print(json.dumps(response.json(), indent=2))

    return (
        (response.json(), None)
        if response.status_code == requests.codes.ok
        else (None, response.json())
    )


def _checkConsentStatusWithSetu(consentHandle):
    """Checks for consent status by hitting the setu api"""

    url = config.SETU_API_BASE_URL + "Consent/handle/" + consentHandle

    headers = createAuthHeadersForSetuAPI({"id": consentHandle})

    response = requests.get(url, headers=headers)

    print(json.dumps(response.json(), indent=2))

    return (
        (response.json(), None)
        if response.status_code == requests.codes.ok
        else (None, response.json())
    )


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


# DATA FLOW


def requestFIDataHandler(user, **kwargs):
    """Requests for data by hitting the Setu API with the consentId and signedConsent"""

    (keys, error) = _generateNewECDHKeys()

    isResponseParsed = kwargs.get("isParsed", False)

    if error:
        # Something went wrong
        print("Couldn't generate keys because, " + error)
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error=error
            )
            if isResponseParsed
            else (None, {"error": error})
        )

    consent = user.consentData.fetch()
    signedConsent = consent.signedConsent
    consentId = consent.consentId

    (resp, error) = _sendDataReqestToSetu(signedConsent, consentId, keys)

    if error:
        # Something went wrong
        print(f"Couldn't request data for {consentId = } because, {str(error)}")
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error=error
            )
            if isResponseParsed
            else (None, {"error": error})
        )

    (newFIData, error) = createFIConsentObj(keys, resp["sessionId"])

    if error:
        # Something went wrong
        print(
            f"Couldn't create data data obj for sessionId = {resp['sessionId']} because, {str(error)}"
        )
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error=error
            )
            if isResponseParsed
            else (None, {"error": error})
        )

    user.fetchFIData = newFIData
    user.save()

    return (
        parseControllerResponse(data={"success": True}, statuscode=200)
        if isResponseParsed
        else (True, None)
    )


def fetchFIDataHandler(fiData, **kwargs):
    """Gets the data from the Setu API after its ready, decrypts it and returns it as an array of data"""

    isResponseParsed = kwargs.get("isParsed", False)

    sessionId = fiData.sessionId
    (resp, error) = _fetchFIDataFromSetu(sessionId)

    if error:
        # Something went wrong
        print(f"Couldn't fetch data for {sessionId = } due to {str(error)}")
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error=error
            )
            if isResponseParsed
            else (None, {"error": error})
        )

    ecdhKey = json.loads(fiData.key)

    data, error = _decryptFIData(resp, ecdhKey)

    if error:
        print("Error decryption failed due to : " + str(error))
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error=error
            )
            if isResponseParsed
            else (None, {"error": error})
        )

    return (
        parseControllerResponse(data={"setu": data}, statuscode=200)
        if isResponseParsed
        else (data, None)
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
        unencodedData = (base64.b64decode(parsedData["base64Data"])).decode("ascii")

        # print(json.dumps(json.loads(unencodedData), indent=4))
        decryptedData.append(json.loads(unencodedData))

    print(type(decryptedData[0]))
    return decryptedData, None


def _generateNewECDHKeys():
    """Hits the Rahasya api to generate new keys needed for data transfer"""

    url = config.RAHASYA_BASE_URL + "generateKey"

    response = requests.get(url)

    print(json.dumps(response.json(), indent=2))

    return (
        (response.json(), None)
        if response.status_code == requests.codes.ok
        else (None, response.json())
    )


def _sendDataReqestToSetu(signedConsent, consentId, keys):
    """Sends Post req to Setu api along with signedConsent, consentId and public keys
    requesting for the user"s data"""
    payload = generateBodyForDataRequest(signedConsent, consentId, keys)

    print(json.dumps(payload, indent=4))

    headers = createAuthHeadersForSetuAPI(payload)

    url = config.SETU_API_BASE_URL + "FI/request"

    response = requests.post(url, headers=headers, json=payload)

    print(json.dumps(response.json(), indent=4))

    return (
        (response.json(), None)
        if response.status_code == requests.codes.ok
        else (None, response.json())
    )


def _fetchFIDataFromSetu(sessionId):
    """Sends a get req to the SETU to get the FI data for the given sessionId"""

    url = config.SETU_API_BASE_URL + "FI/fetch/" + sessionId

    headers = createAuthHeadersForSetuAPI({"sessionId": sessionId})

    response = requests.get(url, headers=headers)

    return (
        (response.json(), None)
        if response.status_code == requests.codes.ok
        else (None, response.json())
    )
