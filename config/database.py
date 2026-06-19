import os
from motor.motor_asyncio import AsyncIOMotorClient

client = None
db = None


async def connect_db():
    global client, db

    mongo_uri = os.environ["MONGO_URL"]
    db_name = os.environ["DB_NAME"]

    client = AsyncIOMotorClient(
        mongo_uri,
        tls=True
    )

    db = client[db_name]

    #testando conexão
    await client.admin.command("ping")

    print("Mongo conectado com sucesso")


def get_db():
    if db is None:
        raise Exception("Banco de dados não conectado")
    return db