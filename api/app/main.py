import dependencies
from beanie import init_beanie, PydanticObjectId
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from routers import geocoder, search, facilities
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from database import db
from models.users import UserCreate, UserRead, UserUpdate, User
from libs.users.user_manager import get_user_manager
from libs.auth import auth_backend


from redis import asyncio as aioredis

origins = ["*"]

fastapi_users = FastAPIUsers[User, PydanticObjectId](
    get_user_manager,
    [auth_backend],
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(geocoder.router)
app.include_router(search.router)
app.include_router(facilities.router)


@app.get("/")
async def root():
    return {"detail": "therapease api"}


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        dependencies.REDIS_URL, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )
