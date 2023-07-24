from typing import Annotated

from fastapi import FastAPI
from routers import geocoder

app = FastAPI()

app.include_router(geocoder.router)


@app.get("/")
async def root():
    return {"message": "therapease api"}
