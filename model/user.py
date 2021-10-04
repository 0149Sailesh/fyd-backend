from mongoengine import Document
from mongoengine.fields import StringField


class User(Document):
    name = StringField(max_length=200, Required=True)
    phone_number = StringField(
        max_length=10, Required=True, primary_key=True)
    password = StringField(Required=True)
