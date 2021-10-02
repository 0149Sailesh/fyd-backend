from pydantic import BaseModel


class __Notifier_NotificationRequestObj(BaseModel):
    type: str
    id: str


class __Notifier_ConsentStatusNotification(BaseModel):
    consentId: str
    consentHandle: str
    consentStatus: str  # ACTIVE | REJECTED | REVOKED | PAUSED


class ConsentNotificationWebhook_Request(BaseModel):
    """Pydantic schema for Consent Request Webhook Notification"""

    ver: str
    timestamp: str
    tnxid: str
    Notifier: __Notifier_NotificationRequestObj
    ConsentStatusNotification: __Notifier_ConsentStatusNotification
