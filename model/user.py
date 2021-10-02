from odmantic import EmbeddedModel, Model, Field
from datetime import datetime
from enum import Enum


class StatusEnum(str, Enum):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ConsentModel(EmbeddedModel):
    consent_id: str
    created_at: datetime = Field(default=datetime.utcnow)
    updated_at: datetime = Field(default=datetime.utcnow)
    data: str
    status: StatusEnum


class UserModel(Model):
    name: str
    password: str
    phone_number: str = Field(primary_field=True)
    consent_data: ConsentModel
