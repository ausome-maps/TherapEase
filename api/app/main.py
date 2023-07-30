from fastapi import FastAPI
from routers import geocoder, search

app = FastAPI()

app.include_router(geocoder.router)
app.include_router(search.router)


@app.get("/")
async def root():
    return {"detail": "therapease api"}
