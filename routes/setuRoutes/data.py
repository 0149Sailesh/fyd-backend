"""All routes related to the FI data requests to the server"""
from fastapi import APIRouter

from controllers.setu import requestFIDataHandler

router = APIRouter()


@router.get("/request")
def requestFIData():
    resp = requestFIDataHandler(isParsed=True)
    if resp["statusCode"] == 200:
        return {"data": resp["data"]}
    return {"error": resp["error"]}
