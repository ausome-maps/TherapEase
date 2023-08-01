from enum import Enum
from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, Field


class FaciltyProperties(BaseModel):
    start: datetime
    end: datetime
    info_src_name: str | None = ""
    info_src_designation: str | None = ""
    placename: str | None = ""
    address: str | None = ""
    region: str | None = ""
    city: str | None = ""
    landmarks_desc: str | None = ""
    contact_number: str | None = ""
    alt_contact_number: str | None = ""
    email_address: str | None = ""
    website: str | None = ""
    social_media: Dict | None = {}  # this will handle facebook and instagram urls
    various_services: Dict | None = {}
    other_services: Dict | None = {}
    caters_to: List | None = []
    images: List | None = []

class Facilities(BaseModel):
    geometry: Dict
    properties: FaciltyProperties
    id: int
