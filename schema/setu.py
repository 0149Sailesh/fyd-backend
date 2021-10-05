from typing import Any, List
from pydantic import BaseModel


class Notifier_NotificationRequestObj(BaseModel):
    type: str
    id: str


class Notifier_ConsentStatusNotification(BaseModel):
    consentId: str
    consentHandle: str
    consentStatus: str  # ACTIVE | REJECTED | REVOKED | PAUSED


class Notifier_FIStatusNotificationNotification(BaseModel):
    sessionId: str
    sessionStatus: str  # ACTIVE | REJECTED | REVOKED | PAUSED
    FIStatusResponse: List[Any]


class ConsentNotificationWebhook_Request(BaseModel):
    """Pydantic schema for Consent Request Webhook Notification"""

    ver: str
    timestamp: str
    txnid: str
    Notifier: Notifier_NotificationRequestObj
    ConsentStatusNotification: Notifier_ConsentStatusNotification


class FINotificationNotificationWebhook_Request(BaseModel):
    """Pydantic schema for FI Data Request Webhook Notification"""

    ver: str
    timestamp: str
    txnid: str
    Notifier: Notifier_NotificationRequestObj
    FIStatusNotification: Notifier_FIStatusNotificationNotification
