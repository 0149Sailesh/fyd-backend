"""All CRUD operations for User, Consent, Data, BlockInfo"""
from datetime import datetime
import json

from model.user import User
from model.consent import Consent, ConsentStatusEnum
from model.data import FIData

from app.helpers import parseControllerResponse


# User CRUD
def findUserWithId(id: str, **kwargs):
    """Finds the user with the given id"""
    isResponseParsed = kwargs.get("isParsed", False)

    try:
        user = User.objects.get(phone_number=id)

        return (
            parseControllerResponse(data={"user": user.to_json()}, statuscode=200)
            if isResponseParsed
            else (user, None)
        )

    except User.DoesNotExist:
        return (
            parseControllerResponse(
                data={"success": False}, statuscode=500, error="User doesnot exist"
            )
            if isResponseParsed
            else (None, "User doesnot exist")
        )
    except Exception as e:
        print(f"couldn't find user with {id = }, becoz {e}")
        return (
            parseControllerResponse(data={"success": False}, statuscode=500, error=e)
            if isResponseParsed
            else (None, {"error": e})
        )


# Consent CRUD


def createConsentObj(phno, consentHandle, **kwargs):
    """Creates a consent obj for the user with the given phone number"""

    isResponseParsed = kwargs.get("isParsed", False)

    try:
        user, error = findUserWithId(phno)

        if user.consentData:
            oldConsentData = user.consentData.fetch()

            if oldConsentData.status.value < 3:
                # user already has provided consent
                return (
                    parseControllerResponse(
                        data={"success": False},
                        statuscode=400,
                        error="User already has provided consent",
                    )
                    if isResponseParsed
                    else (False, "User already has provided consent")
                )

            oldConsentData.consentHandle = ""
            oldConsentData.createdAt = datetime.utcnow()
            oldConsentData.updatedAt = datetime.utcnow()
            oldConsentData.status = ConsentStatusEnum.PENDING
            oldConsentData.signedConsent = ""
            oldConsentData.consentHandle = consentHandle
            oldConsentData.save()

            return (
                parseControllerResponse(
                    data={"user": user.to_json(), "consent": oldConsentData.to_json()},
                    statuscode=200,
                )
                if isResponseParsed
                else (True, None)
            )

        if error:
            return (
                parseControllerResponse(
                    data={"success": False}, statuscode=500, error=error
                )
                if isResponseParsed
                else (False, error)
            )

        newConsent = Consent(consentHandle=consentHandle)
        newConsent.save()
        user.consentData = newConsent
        user.save()

        return (
            parseControllerResponse(
                data={"user": user.to_json(), "consent": newConsent.to_json()},
                statuscode=200,
            )
            if isResponseParsed
            else (True, None)
        )

    except Exception as e:
        print(
            f"couldn't create consent for user with {phno = } and {consentHandle = }, becoz {e}"
        )
        return (
            parseControllerResponse(data={"success": False}, statuscode=500, error=e)
            if isResponseParsed
            else (False, {"error": e})
        )


def updateConsentStatusAndConsentId(consentHandle, consentId, newStatus, **kwargs):
    """Updates consentId, consentStatus for given consentHandle"""
    isResponseParsed = kwargs.get("isParsed", False)

    try:
        consent = Consent.objects.get(consentHandle=consentHandle)

        consent.consentId = consentId
        consent.status = ConsentStatusEnum[newStatus]
        consent.save()

        return (
            parseControllerResponse(data={"consent": consent.to_json()}, statuscode=200)
            if isResponseParsed
            else (consent, None)
        )

    except Consent.DoesNotExist:
        return (
            parseControllerResponse(
                data={"success": False},
                statuscode=500,
                error="ConsentHandle does not exist",
            )
            if isResponseParsed
            else (None, "ConsentHandle doesnot exist")
        )
    except Exception as e:
        print(
            f"couldn't update consent with with {consentHandle = }, {consentId= }, {newStatus = }, becoz {e}"
        )
        return (
            parseControllerResponse(data={"success": False}, statuscode=500, error=e)
            if isResponseParsed
            else (None, {"error": e})
        )


def updateSignedConsent(consentHandle, signedConsent, fetchCount, **kwargs):
    """Updates the signedConsent for the given consentHandle"""
    isResponseParsed = kwargs.get("isParsed", False)

    try:
        consent = Consent.objects.get(consentHandle=consentHandle)
        consent.signedConsent = signedConsent
        consent.fetchCount = int(fetchCount)

        consent.save()

        return (
            parseControllerResponse(data={"consent": consent.to_json()}, statuscode=200)
            if isResponseParsed
            else (consent, None)
        )

    except Consent.DoesNotExist:
        return (
            parseControllerResponse(
                data={"success": False},
                statuscode=500,
                error="Consent Handle does not exist",
            )
            if isResponseParsed
            else (None, "ConsentHandle doesnot exist")
        )

    except Exception as e:
        print(f"Updates the signedConsent for the given {consentHandle = }, becoz {e}")
        return (
            parseControllerResponse(data={"success": False}, statuscode=500, error=e)
            if isResponseParsed
            else (None, {"error": e})
        )


# FI Data CRUD


def createFIConsentObj(key, sessionId, **kwargs):
    """Creates a new FI Consent Obj with the given key and sessionId"""

    isResponseParsed = kwargs.get("isParsed", False)

    try:
        newFIData = FIData(sessionId=sessionId)
        stringifiedKey = json.dumps(key)
        newFIData.key = stringifiedKey

        newFIData.save()

        return (
            parseControllerResponse(
                data={"FIData": newFIData.to_json()},
                statuscode=200,
            )
            if isResponseParsed
            else (newFIData, None)
        )

    except Exception as e:
        print(f"couldn't create FIData for user with and {sessionId = }, becoz {e}")
        return (
            parseControllerResponse(data={"success": False}, statuscode=500, error=e)
            if isResponseParsed
            else (False, {"error": e})
        )
