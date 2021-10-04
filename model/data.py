from mongoengine import Document
from mongoengine.fields import DateField, DateTimeField, ReferenceField, StringField

from datetime import datetime
from model.user import User

status_choices = ("approved", "pending", "rejected", "expired", "revoked")


class Data(Document):
    owner = ReferenceField(User)
    consent_handle = StringField()
    consent_id = StringField()
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
    status = StringField(choices=status_choices)
