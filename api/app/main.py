import dependencies
from fastapi import FastAPI
from routers import geocoder, search, facilities
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

app = FastAPI()

app.include_router(geocoder.router)
app.include_router(search.router)
app.include_router(facilities.router)


@app.get("/")
async def root():
    return {"detail": "therapease api"}

@app.on_event("startup")
async def startup():
    print(dependencies.REDIS_URL)
    redis = aioredis.from_url(dependencies.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")