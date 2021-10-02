from datetime import datetime
import enum

from app.config import config


def convertDateToISOFormat(date: datetime):
    """Converts the given datetime obj to a
    ISO format string with Z and T"""
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


def parseControllerResponse(data, statuscode: int, **kwargs):
    error = kwargs.get("error", None)
    message = kwargs.get("message", None)

    class Statuscode(enum.Enum):
        Success = 200
        BadRequest = 400  # wrong data
        Unauthorized = 401  # unauthenticated users
        Forbidden = 403  # authenticated, but not authorized to view the page
        NotFound = 404
        InternalServerError = 500
        DuplicateKey = 11000  # Mongo throws a 11000 error when there is a duplicate key

    # Generic error message for production env
    if not config.DEBUG and statuscode == 500:
        error = "Something went wrong, try again later"

    resp = {
        "data": data,
        "statusCode": statuscode,
        "success": statuscode == 200,
        "statusMessage": (Statuscode(statuscode)).name,
        "error": error if error else None,
        "message": message if message else None,
    }

    # set duplicate key error status code to 400
    if resp["statusCode"] == 11000:
        resp["statusCode"] = 400

    return resp
