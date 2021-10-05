from mongoengine import Document
from mongoengine.fields import (
    DateField,
    DateTimeField,
    ReferenceField,
    StringField,
    EnumField,
)
from enum import Enum

from datetime import datetime
from model.user import User


status_choices = ("approved", "pending", "rejected", "expired", "revoked")


def consentStatusHelper(key):
    return {
        "1": "User has given consent",
        "2": "Requested user for consent",
        "3": "User rejected consent request",
        "4": "User revoked consent request",
        "5": "Consent approval expired"
        # BUG: we wont know if the consent has expired, (can
        # be ignored for now, as consent length = 1 year )
    }[key]


class ConsentStatusEnum(Enum):
    APPROVED = 1
    PENDING = 2
    REJECTED = 3
    REVOKED = 4
    EXPIRED = 5


class Consent(Document):
    """Consent Model"""

    owner = ReferenceField(User)
    consent_handle = StringField()
    consent_id = StringField()
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
    status = EnumField(ConsentStatusEnum, default=ConsentStatusEnum.PENDING)
    signed_consent = StringField(default="")
