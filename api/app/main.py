import dependencies
from fastapi import FastAPI
from routers import geocoder, search, facilities
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware

from db import create_db_and_tables
from models.users import UserCreate, UserRead, UserUpdate
from libs.users import auth_backend, fastapi_users


from redis import asyncio as aioredis

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
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
    await create_db_and_tables()
