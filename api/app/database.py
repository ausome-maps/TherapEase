import dependencies
import motor.motor_asyncio
# from beanie import Document
# from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

client = motor.motor_asyncio.AsyncIOMotorClient(
    dependencies.DATABASE_URL, uuidRepresentation="standard"
)

db = client[dependencies.MONGO_INITDB_DATABASE]

# class User(BeanieBaseUser, Document):
#     name: str


# async def get_user_db():
#     yield BeanieUserDatabase(User)