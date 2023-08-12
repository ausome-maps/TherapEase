import dependencies
from fastapi import FastAPI
from routers import geocoder, search, facilities, auth, users
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware


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
app.include_router(geocoder.router)
app.include_router(search.router)
app.include_router(facilities.router)
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"detail": "therapease api"}


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        dependencies.REDIS_URL, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
