import dependencies
from fastapi import APIRouter, Request
from models.facilities import Facilities
from libs.search.full_text import FullTextSearch
from libs.facilities.transform import transform_es_result_to_geojson

router = APIRouter()


@router.put("/facilities")
async def facilities_store_url(facilities: Facilities):
    """
     Stores facilities in FullTextSearch. This is a low - level function to be used by clients that want to store a set of facilities in a full text search.
     
     @param facilities - A list of : class : ` ~faker. models. facilities. Facilities `.
     
     @return The response from the search request as a JSON object. Example usage. code - block :: python import fts >>> urls = await facilities_store_url
    """
    fts = FullTextSearch()
    resp = fts.put(facilities.model_dump_json(),  dependencies.SEARCH_URL + f'/facilities/_doc/{facilities.model_dump()["id"]}')
    return resp

@router.get('/facilities')
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
    resp = fts.get(request.query_params, dependencies.SEARCH_URL + '/facilities/_search')
    return transform_es_result_to_geojson(resp["hits"]["hits"])
    