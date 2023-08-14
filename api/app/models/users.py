
from beanie import PydanticObjectId
from typing import Optional

from fastapi_users import schemas

from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

class User(BeanieBaseUser, Document):
    name: str

async def get_user_db():
    yield BeanieUserDatabase(User)

class UserRead(schemas.BaseUser[PydanticObjectId]):
    name: str


class UserCreate(schemas.BaseUserCreate):
    name: str


class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str]
