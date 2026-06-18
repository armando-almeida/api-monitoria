import os
from motor.motor_asyncio import AsyncIOMotorClient

client = None
db = None

async def connect_db():
    global client, db
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")
    
    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    print("Conectado ao MongoDB")

def get_db():
    if db is None:
        raise Exception("Banco de dados não conectado")
    return db