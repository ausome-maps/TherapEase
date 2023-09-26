from fastapi import APIRouter, Request, Depends
from app.models.facilities import Facilities
from app.libs.search.full_text import FullTextSearch
from app.libs.facilities.transform import transform_es_result_to_geojson
from app.libs.users import current_active_user
from app.config import get_settings
from app.db import User

router = APIRouter()

settings = get_settings()


@router.put("/facilities")
async def facilities_store_url(
    facilities: Facilities,
    request: Request,
    user: User = Depends(current_active_user),
):
    """
    Stores facilities in FullTextSearch. This is a low - level function to be used by clients that want to store a set of facilities in a full text search.

    @param facilities - A list of : class : ` ~faker. models. facilities. Facilities `.

    @return The response from the search request as a JSON object. Example usage. code - block :: python import fts >>> urls = await facilities_store_url
    """
    fts = FullTextSearch()
    if request.cookies.get("key") != settings.FASTAPI_SECRET_KEY:
        return {"detail": "Invalid secret key"}
    resp = fts.put(
        facilities.model_dump_json(),
        settings.SEARCH_URL + f'/facilities/_doc/{facilities.model_dump()["id"]}',
    )
    return resp


@router.get("/facilities")
async def facilities_fetch_url(request: Request):
    """
    Fetch facilities from FullText Search. This is a wrapper around the full text search API which does not require a query parameter

    @param request - The request to be processed

    @return A GeoJSON representation of the
    """
    # Returns a message if no query parameters are supplied.
    if len(request.query_params) == 0:
        return {"message": "No supplied query for searching."}
    fts = FullTextSearch()
    resp = fts.get(request.query_params, settings.SEARCH_URL + "/facilities/_search")
    return transform_es_result_to_geojson(resp)


@router.post("/facilities")
async def facilities_fetch_url(request: Request):
    """
    Fetch facilities from FullText Search. This is a wrapper around the full text search API which does not require a query parameter

    @param request - The request to be processed

    @return A GeoJSON representation of the
    """
    # Returns a message if no query parameters are supplied.
    fts = FullTextSearch()
    data_query = await request.json()
    resp = fts.post(data_query, settings.SEARCH_URL + "/facilities/_search")
    return transform_es_result_to_geojson(resp)
