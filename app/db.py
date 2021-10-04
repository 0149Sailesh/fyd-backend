import mongoengine


from mongoengine import connect
from app.config import config


def connect_db():
    connect(config.DB_NAME)
