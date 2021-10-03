from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine, engine

from app.config import config

# engine will be used to access all collections in db i.e to run queries


def connect_db():
    engine = AIOEngine(database=config.DB_NAME)
    return engine
