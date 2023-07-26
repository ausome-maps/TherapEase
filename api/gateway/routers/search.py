from fastapi import APIRouter, Request
from libs.search.full_text import FullTextSeaerch

router = APIRouter()


@router.get("/search")
async def search_url(request: Request):
    """
     Search for full text. This is a shortcut for : func : ` FullTextSeaerch. get `
     
     @param request - The request to get the URL from.
     
     @return The URL to send to the client for the search or an error message if there was a problem.
    """
    # Returns a message to display when the request is None.
    if request is None:
        return {"message": "No supplied query for searching."}
    fts = FullTextSeaerch()
    return fts.get(request.query_params).json()
