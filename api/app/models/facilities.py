from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

DEFAULT_SERVICES_OFFERED = {
    "speechlanguagetherapy": {
        "label": "Speech-Language Therapy",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "speechlanguagepathology": {
        "label": "Speech-Language Pathology",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "occupationaltherapy": {
        "label": "Occupational Therapy",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "behavioraltherapy": {
        "label": "Behavioral Therapy",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "physicaltherapy": {
        "label": "Physical Therapy",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "lifeskillstraining": {
        "label": "Life Skills Training",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "socialskillstraining": {
        "label": "Social Skills Training",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "integration": {
        "label": "Integration",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "integrationprogram": {
        "label": "Integration Program",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "jobcoaching": {
        "label": "Job Coaching",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "specialeducation": {
        "label": "Special Education",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "spedtutorials": {
        "label": "SpEd Tutorials",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "parentcoaching": {
        "label": "Parent Coaching",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "educationsessionforfamilies": {
        "label": "Education Session for Families",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "feeding": {
        "label": "Feeding",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "counseling": {
        "label": "Counseling",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "psychotherapy": {
        "label": "Psychotherapy",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "abatherapy": {
        "label": "ABA Therapy",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "mnri": {
        "label": "MNRI",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "sensoryintegration": {
        "label": "Sensory Integration",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "playschool": {
        "label": "Play School",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "dysphagiamanagement": {
        "label": "Dysphagia Management",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "orthoses": {
        "label": "Orthoses (Splinting)",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "homeschoolfacilitation": {
        "label": "Homeschool Facilitation",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
    "rehabconsultation": {
        "label": "Rehab Consultation",
        "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
    },
}

DEFAULT_ACCREDITATION = {"paot": 0, "pasp": 0}


class FaciltyProperties(BaseModel):
    osm_id: str | None = ""
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
    services_offered: Dict | None = DEFAULT_SERVICES_OFFERED
    other_services: str | None = ""
    caters_to: List | None = []
    images: List | None = []
    accreditation: Dict | None = DEFAULT_ACCREDITATION


class Facilities(BaseModel):
    geometry: Dict
    properties: FaciltyProperties
    id: str
