from fastapi import APIRouter
from fastapi import Request
from libs.search.nominatim import NominatimSearch

router = APIRouter()


@router.get("/geocode")
async def geocode_url(request: Request):
    """
     Geocoding service. This is a shortcut for : func : ` NominatimSearch. get `
     It is used to retrieve information about the location and its location's latitude and longitude
     
     @param request - The request that contains the URL query parameters. Refer to the following link for the list of parameters: https://nominatim.org/release-docs/latest/api/Search/
     
     @return The URL to be used to retrieve the location and its location's latitude and longitude.
    """
    # Return the geocode_url as a JSON string.
    if len(request.query_params) == 0:
        return {"message": "No supplied query for geocoding."}
    ns = NominatimSearch()
    return ns.get(request.query_params)
