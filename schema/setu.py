from pydantic import BaseModel


class Notifier_NotificationRequestObj(BaseModel):
    type: str
    id: str


class Notifier_ConsentStatusNotification(BaseModel):
    consentId: str
    consentHandle: str
    consentStatus: str  # ACTIVE | REJECTED | REVOKED | PAUSED


class ConsentNotificationWebhook_Request(BaseModel):
    """Pydantic schema for Consent Request Webhook Notification"""

    ver: str
    timestamp: str
    txnid: str
    Notifier: Notifier_NotificationRequestObj
    ConsentStatusNotification: Notifier_ConsentStatusNotification
