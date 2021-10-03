"""All consent Routes for the app"""

from fastapi import APIRouter

from controllers.setu import createAConsentRequestHandler, checkConsentStatusHandler

router = APIRouter()


@router.get(
    "",
)
def requestForUserConsent():
    return {"route": "setu consent route"}


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
