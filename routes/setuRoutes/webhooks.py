"""All webhook routes"""

from fastapi import APIRouter, Body

from controllers.setu_webhooks import consentWebHookNotificationHandler
from schema.setu import ConsentNotificationWebhook_Request

router = APIRouter()


@router.post("/consent/notification")
def consentWebhookNotification(
    consentData: ConsentNotificationWebhook_Request = Body(...),
):
    return consentWebHookNotificationHandler(consentData.ConsentStatusNotification)
