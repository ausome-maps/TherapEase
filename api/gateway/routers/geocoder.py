from fastapi import APIRouter
from fastapi import Request
from libs.search.nominatim import NominatimSeaerch

router = APIRouter()


@router.get("/geocode")
async def geocode_url(request: Request):
    """
     Returns the geocode URL. It is used to retrieve information about the location and its location's latitude and longitude
     
     @param request - The request that contains the URL query parameters
     
     @return The URL to be used to retrieve the location and its location's latitude and longitude.
    """
    # Return the geocode_url as a JSON string.
    print('hello')
    if request is None:
        return {"message": "No supplied query for geocoding."}
    ns = NominatimSeaerch()
    return ns.get(request.query_params).json()
