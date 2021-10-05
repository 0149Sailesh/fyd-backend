"""All consent Routes for the app"""

from fastapi import APIRouter, Depends

from controllers.setu import (
    createAConsentRequestHandler,
    checkConsentStatusHandler,
    fetchSignedConsentHandler,
)
from controllers.user import createConsentObj

from utils.auth import auth_handler
from app.helpers import ErrorResponseModel, ResponseModel

router = APIRouter()


@router.get("")
def dummyRoute(user_id=Depends(auth_handler.auth_wrapper)):

    return {"phNo": user_id}


@router.get("/request")
def requestForUserConsent(userId=Depends(auth_handler.auth_wrapper)):
    resp, error = createAConsentRequestHandler(userId, isParsed=False)
    if error:
        return ErrorResponseModel(error, 500, message="Error while requesting for data")
    _, error = createConsentObj(userId, resp["ConsentHandle"])

    if error:
        statuscode = 400 if error == "User already has provided consent" else 500
        return ErrorResponseModel(
            error, statuscode, message="Error while storing consent data to db"
        )

    return ResponseModel(
        data={"success": True, "consentHandle": resp["ConsentHandle"]},
        message="Successfully requested for consent",
    )


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
