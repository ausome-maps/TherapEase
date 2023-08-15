from typing import List
from fastapi import APIRouter, Request, Depends
from models.facilities import Facilities
from libs.search.full_text import FullTextSearch
from libs.facilities.transform import transform_es_result_to_geojson
from libs.auth import current_active_user
from models.users import UserRead, User
import dependencies

router = APIRouter()


@router.put("/facilities", dependencies=[Depends(current_active_user)])
async def facilities_store_url(facilities: Facilities):
    """
    Stores facilities in FullTextSearch. This is a low - level function to be used by clients that want to store a set of facilities in a full text search.

    @param facilities - A list of : class : ` ~faker. models. facilities. Facilities `.

    @return The response from the search request as a JSON object. Example usage. code - block :: python import fts >>> urls = await facilities_store_url
    """
    fts = FullTextSearch()
    resp = fts.put(
        facilities.model_dump_json(),
        dependencies.SEARCH_URL + f'/facilities/_doc/{facilities.model_dump()["id"]}',
    )
    return resp


@router.get("/facilities")
async def facilities_fetch_url(request: Request):
    """
    Fetches facilities by query. This is a view that uses FullTextSearch to perform a search and returns a GeoJSON object.

    @param request - The request for this endpoint. Required. The URL that we need to make a request to.

    @return A GeoJSON object containing the query results of the facilities.
    """
    # Returns a message if no query parameters are supplied.
    if len(request.query_params) == 0:
        return {"message": "No supplied query for searching."}
    fts = FullTextSearch()
    resp = fts.get(
        request.query_params, dependencies.SEARCH_URL + "/facilities/_search"
    )
    return transform_es_result_to_geojson(resp)


@router.get("/facilities-users", response_model=List[User])
async def list_users():
    # u = await User.find_one({"email": "admin@sample.com"})
    # await u.set({User.is_verified: True})
    u = await User.find_all().to_list()
    return u
