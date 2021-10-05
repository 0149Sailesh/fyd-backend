"""All consent Routes for the app"""

from fastapi import APIRouter, Depends

from controllers.setu import (
    createAConsentRequestHandler,
    checkConsentStatusHandler,
    fetchSignedConsentHandler,
)
from controllers.user import (
    createConsentObj,
    findUserWithId,
    updateConsentStatusAndConsentId,
)

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


@router.get("/check")
def checkConsentStatus(userId=Depends(auth_handler.auth_wrapper)):
    user, error = findUserWithId(userId)
    if error:
        return ErrorResponseModel(error, 401, message="Invalid user id")
    consent = user.consentData.fetch()
    resp, error = checkConsentStatusHandler(consent.consentHandle)
    if error:
        return ErrorResponseModel(
            error={
                "error": error,
                "message": "something went wrong while checking consent status",
            },
            statuscode=500,
            message="something went wrong while checking consent status",
        )

    if resp["ConsentStatus"]["status"] == "READY":
        resp["ConsentStatus"]["status"] = "ACTIVE"
    if resp["ConsentStatus"]["status"] == "FAILED":
        resp["ConsentStatus"]["status"] = "REJECTED"

    _, error = updateConsentStatusAndConsentId(
        consent.consentHandle,
        resp["ConsentStatus"]["id"],
        resp["ConsentStatus"]["status"],
    )

    if error:
        return ErrorResponseModel(
            error={
                "error": error,
                "message": "something went wrong while checking consent status",
            },
            statuscode=500,
            message="something went wrong while checking consent status",
        )

    return ResponseModel(
        data={"success": True, "status": resp["ConsentStatus"]["status"]},
        message="Successfully requested for consent",
    )


@router.get("/fetch/{consentId}")
def fetchSignedConsent(consentId: str):
    resp = fetchSignedConsentHandler(consentId=consentId, isParsed=True)
    if resp["statusCode"] == 200:
        return {"data": resp["data"]}
    return {"error": resp["error"]}
