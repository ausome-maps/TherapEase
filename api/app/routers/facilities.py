import dependencies
from fastapi import APIRouter
from models.facilities import Facilities
from libs.search.full_text import FullTextSearch

router = APIRouter()


@router.put("/facilities")
async def facilities_store_url(facilities: Facilities):
    fts = FullTextSearch()
    resp = fts.put(facilities.json(),  dependencies.SEARCH_URL + f'/facilities/_doc/{facilities.dict()["id"]}')
    return resp
