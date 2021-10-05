from mongoengine import Document
from mongoengine.fields import StringField, EnumField
from enum import Enum
import json

from datetime import datetime
from model.user import User


def dataStatusHelper(key):
    return {
        "1": "Request for data",
        "2": "Data is being fetched from the API. Please wait.",
        "3": "Data is ready.",
    }[key]


class DataStatusEnum(Enum):
    BEGIN_REQUEST = 1
    PROCESSING = 2
    READY = 3


class FIData(Document):
    """Consent Model"""

    key = StringField()  # stringified key ECDH key obj
    sessionId = StringField(default="")
    status = EnumField(DataStatusEnum, default=DataStatusEnum.BEGIN_REQUEST)

    def parseKey(self):
        return json.loads(self.key)

    @classmethod
    def stringifyKey(key):
        return json.dump(key)
