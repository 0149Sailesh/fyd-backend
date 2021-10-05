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
    updateSignedConsent,
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
    """NOTE: If the status is ACTIVE, call the /fetch route immediately"""
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


@router.get("/fetch")
def fetchSignedConsent(userId=Depends(auth_handler.auth_wrapper)):
    user, error = findUserWithId(userId)
    if error:
        return ErrorResponseModel(error, 401, message="Invalid user id")
    consent = user.consentData.fetch()
    if consent.status.value != 1:
        return ErrorResponseModel(
            error={
                "error": "Insufficient permissions",
            },
            statuscode=400,
            message="Insufficient permissions",
        )
    resp, error = fetchSignedConsentHandler(consent.consentId)
    if error:
        return ErrorResponseModel(
            error={
                "error": error,
                "message": "something went wrong while fetching signed consent",
            },
            statuscode=500,
            message="something went wrong while fetching signed consent",
        )
    resp, error = updateSignedConsent(
        consent.consentHandle, resp["signedConsent"], resp["ConsentUse"]["count"]
    )

    if error:
        return ErrorResponseModel(
            error={
                "error": error,
                "message": "something went wrong while fetching signed consent",
            },
            statuscode=500,
            message="something went wrong while fetching signed consent",
        )

    return ResponseModel(
        data={"success": True},
        message="Successfully fetched signed consent",
    )
