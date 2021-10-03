from pydantic import BaseModel


class _Notifier_NotificationRequestObj(BaseModel):
    type: str
    id: str


class _Notifier_ConsentStatusNotification(BaseModel):
    consentId: str
    consentHandle: str
    consentStatus: str  # ACTIVE | REJECTED | REVOKED | PAUSED


class ConsentNotificationWebhook_Request(BaseModel):
    """Pydantic schema for Consent Request Webhook Notification"""

    ver: str
    timestamp: str
    tnxid: str
    Notifier: _Notifier_NotificationRequestObj
    ConsentStatusNotification: _Notifier_ConsentStatusNotification
