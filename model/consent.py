from mongoengine import Document
from mongoengine.fields import (
    DateField,
    DateTimeField,
    IntField,
    StringField,
    EnumField,
)
from enum import Enum

from datetime import datetime


def consentStatusHelper(key):
    return {
        "1": "User has given consent",
        "2": "Requested user for consent",
        "3": "User rejected consent request",
        "4": "User revoked consent request",
        "5": "Consent approval expired",
        "6": "Consent Approval has been paused"
        # BUG: we wont know if the consent has expired, (can
        # be ignored for now, as consent length = 1 year )
    }[key]


class ConsentStatusEnum(Enum):
    ACTIVE = 1
    PENDING = 2
    REJECTED = 3
    REVOKED = 4
    EXPIRED = 5
    PAUSED = 6


class Consent(Document):
    """Consent Model"""

    consentHandle = StringField(Required=True, unique=True)
    consentId = StringField(unique=True)
    createdAt = DateTimeField(default=datetime.utcnow())
    updatedAt = DateTimeField(default=datetime.utcnow())
    status = EnumField(ConsentStatusEnum, default=ConsentStatusEnum.PENDING)
    signedConsent = StringField(default="")
    fetchCount = IntField(default=1)
