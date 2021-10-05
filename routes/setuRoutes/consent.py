"""All consent Routes for the app"""

from fastapi import APIRouter, Depends

from controllers.setu import (
    createAConsentRequestHandler,
    checkConsentStatusHandler,
    fetchSignedConsentHandler,
)

from utils.auth import auth_handler

router = APIRouter()


@router.get("")
def requestForUserConsent(user_id=Depends(auth_handler.auth_wrapper)):

    return {"route": user_id}


@router.get("/request")
def requestForUserConsent():
    mobileNumber = "9999999999"
    resp = createAConsentRequestHandler(mobileNumber, isParsed=True)
    if resp["statusCode"] == 200:
        return {"data": resp["data"]}
    return {"error": resp["error"]}


@router.get("/check/{consentHandle}")
def checkConsentStatus(consentHandle: str):
    resp = checkConsentStatusHandler(consentHandle=consentHandle, isParsed=True)
    if resp["statusCode"] == 200:
        return {"data": resp["data"]}
    return {"error": resp["error"]}


@router.get("/fetch/{consentId}")
def fetchSignedConsent(consentId: str):
    resp = fetchSignedConsentHandler(consentId=consentId, isParsed=True)
    if resp["statusCode"] == 200:
        return {"data": resp["data"]}
    return {"error": resp["error"]}
