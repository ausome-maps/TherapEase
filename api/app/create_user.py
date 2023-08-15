import contextlib
import asyncio
from models.users import User, UserCreate
from beanie import init_beanie
from database import db
from libs.users.user_manager import get_user_manager, get_user_db
from fastapi_users.exceptions import UserAlreadyExists

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: str = "root@admin.com",
    password: str = "rootpassword1234",
    is_superuser: bool = True,
):
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )
    try:
        async with get_user_db_context() as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                await user_manager.create(
                    UserCreate(
                        name="admin name",
                        email=email,
                        password=password,
                        is_active=True,
                        is_verified=True,
                        is_superuser=is_superuser,
                    )
                )
    except UserAlreadyExists:
        print(f"User {email} already exists")


if __name__ == "__main__":
    asyncio.run(create_user())
