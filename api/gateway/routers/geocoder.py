from typing import Union
from fastapi import APIRouter
import requests
import dependencies

router = APIRouter()


@router.get("/geocode")
async def geocode_url(q: Union[str, None] = None):
    geocode_url = dependencies.GEOCODING_URL
    if q is None:
        return {"message": geocode_url}
    query_params = {"q": q}
    print(geocode_url, query_params)
    r = requests.get(geocode_url, params=query_params)
    print(r.text, r.status_code)
    return r.json()
