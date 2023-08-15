from beanie import PydanticObjectId
from typing import Optional

from fastapi_users import schemas

from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase


class User(BeanieBaseUser, Document):
    name: str


class UserRead(schemas.BaseUser[PydanticObjectId]):
    name: str


class UserCreate(schemas.BaseUserCreate):
    name: str
    email: str


class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str]


async def get_user_db():
    """
    Get User database. This is a fixture to allow unit tests to use it without having to write code
    """
    yield BeanieUserDatabase(User)
