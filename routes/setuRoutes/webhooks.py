"""All webhook routes"""

from fastapi import APIRouter, Body

from controllers.setu_webhooks import (
    consentWebHookNotificationHandler,
    fiDataWebHookNotificationHandler,
)
from schema.setu import (
    ConsentNotificationWebhook_Request,
    FINotificationNotificationWebhook_Request,
)

router = APIRouter()


@router.post("/consent/notification")
def consentWebhookNotification(
    consentData: ConsentNotificationWebhook_Request = Body(...),
):
    return consentWebHookNotificationHandler(consentData.ConsentStatusNotification)


@router.post("/fi/notification")
def consentWebhookNotification(
    fiData: FINotificationNotificationWebhook_Request = Body(...),
):
    return fiDataWebHookNotificationHandler(fiData.FIStatusNotification.sessionId)
