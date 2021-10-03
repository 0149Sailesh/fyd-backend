from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from app.config import config

client = AsyncIOMotorClient("mongodb://localhost:27017/")

# engine will be used to access all collections in db i.e to run queries
engine = AIOEngine(motor_client=client, database=config.DB_NAME)
