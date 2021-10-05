"""All routes related to the FI data requests to the server"""
from fastapi import APIRouter, Depends

from controllers.setu import fetchFIDataHandler, requestFIDataHandler
from controllers.user import findUserWithId

from utils.auth import auth_handler

from app.helpers import ErrorResponseModel, ResponseModel

router = APIRouter()


@router.get("/request")
def requestFIData(user_id=Depends(auth_handler.auth_wrapper)):
    user, error = findUserWithId(user_id)
    if error:
        return ErrorResponseModel(error, 401, message="Invalid user id")
    consent = user.consentData.fetch()
    if not consent.signedConsent:
        return ErrorResponseModel(
            error={
                "error": "Insufficient data",
            },
            statuscode=400,
            message="Insufficient data",
        )
    _, error = requestFIDataHandler(user)
    if error:
        return ErrorResponseModel(
            error={
                "error": error,
                "message": "something went wrong while requesting for FI Data",
            },
            statuscode=500,
            message="something went wrong while requesting for FI Data",
        )

    return ResponseModel(
        data={"success": True},
        message="Successfully fetched signed consent",
    )


@router.get("/fetch")
def fetchFIData(user_id=Depends(auth_handler.auth_wrapper)):
    user, error = findUserWithId(user_id)
    if error:
        return ErrorResponseModel(error, 401, message="Invalid user id")
    fiData = user.fetchFIData.fetch()
    if fiData.status.value != 3:
        return ErrorResponseModel(
            error={
                "error": "Data not ready",
            },
            statuscode=400,
            message="Data not ready",
        )
    resp, error = fetchFIDataHandler(fiData)
    if error:
        return ErrorResponseModel(
            error={
                "error": error,
                "message": "something went wrong while fetching for FI Data",
            },
            statuscode=500,
            message="something went wrong while fetching for FI Data",
        )

    fiData.delete()
    
    return ResponseModel(
        data={"data": resp},
        message="Successfully fetched signed consent",
    )
