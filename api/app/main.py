from fastapi import FastAPI
from routers import geocoder, search, facilities

app = FastAPI()

app.include_router(geocoder.router)
app.include_router(search.router)
app.include_router(facilities.router)


@app.get("/")
async def root():
    return {"detail": "therapease api"}
