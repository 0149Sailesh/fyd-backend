from mongoengine import Document, NULLIFY
from mongoengine.fields import StringField, LazyReferenceField


from .consent import Consent
from .data import FIData


class User(Document):
    name = StringField(max_length=200, Required=True)
    phone_number = StringField(max_length=10, Required=True, primary_key=True)
    password = StringField(Required=True)
    consentData = LazyReferenceField(Consent, reverse_delete_rule=NULLIFY, default=None)
    fetchFIData = LazyReferenceField(FIData, reverse_delete_rule=NULLIFY, default=None)
