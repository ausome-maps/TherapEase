from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis
from app.endpoints import geocoder, search, facilities, users
from app.config import get_settings

from app.db import create_db_and_tables

origins = ["*"]
settings = get_settings()
app = FastAPI()


@app.get("/")
async def root():
    return {"detail": "therapease api"}


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        get_settings().REDIS_URL, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await create_db_and_tables()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(geocoder.router, tags=["Geocoder"])
app.include_router(search.router, tags=["Search"])
app.include_router(facilities.router, tags=["Facilities"])
app.include_router(users.router)


@app.get("/")
async def root():
    return {"detail": "therapease api"}
