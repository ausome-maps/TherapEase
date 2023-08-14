import dependencies
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    dependencies.DATABASE_URL, uuidRepresentation="standard"
)

db = client[dependencies.MONGO_INITDB_DATABASE]