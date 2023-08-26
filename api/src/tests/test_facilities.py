import requests
import json
import time
from fastapi.testclient import TestClient
from app.config import get_settings
from app.main import app
from app.libs.search.full_text import FullTextSearch

client = TestClient(app)

settings = get_settings()

data = {
    "id": "2505150",
    "geometry": {"type": "Point", "coordinates": [121.033888, 14.564758]},
    "properties": {
        "osmid": "",
        "accreditation": {"paot": 1, "pasp": 1},
        "date_updated": "2023-07-19T22:43:32.508+08:00",
        "info_src_name": "Pilar Balboa",
        "info_src_designation": "",
        "placename": "Play Explorers Therapy Center",
        "desc_long": "",
        "desc_short": "",
        "address": "2396 Leon Guinto St, Malate, Manila",
        "region": "NCR \u2013 National Capital Region",
        "city": "Manila City",
        "province": "",
        "landmarks_desc": "Our Lady of Fatima Parish",
        "contact_number_mobile": "0917 838 9939",
        "contact_number_landline": "",
        "alt_contact_numbers": "",
        "email_address": "playexplorerstherapycenter@gmail.com",
        "alt_email_address": "",
        "website": "",
        "social_media": {"facebook": "", "instagram": ""},
        "caters_to": ["Pediatric"],
        "other_services": "Dance Classes, Physical Therapy for Pediatrics",
        "images": [
            {"img_name": "download (3)-22_38_28.jpg", "img_url": ""},
            {"img_name": "download (4)-22_38_49.jpg", "img_url": ""},
        ],
        "services_offered": {
            "speechlanguagetherapy": {
                "label": "Speech-Language Therapy",
                "mode": {"teletherapy": 0, "onsite": 1, "home_service": 0},
            },
            "speechlanguagepathology": {
                "label": "Speech-Language Pathology",
                "mode": {"teletherapy": 0, "onsite": 1, "home_service": 0},
            },
            "occupationaltherapy": {
                "label": "Occupational Therapy",
                "mode": {"teletherapy": 0, "onsite": 1, "home_service": 0},
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
                "mode": {"teletherapy": 0, "onsite": 2, "home_service": 0},
            },
            "socialskillstraining": {
                "label": "Social Skills Training",
                "mode": {"teletherapy": 0, "onsite": 2, "home_service": 0},
            },
            "integration": {
                "label": "Integration",
                "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
            },
            "integrationprogram": {
                "label": "Integration Program",
                "mode": {"teletherapy": 0, "onsite": 2, "home_service": 0},
            },
            "jobcoaching": {
                "label": "Job Coaching",
                "mode": {"teletherapy": 0, "onsite": 2, "home_service": 0},
            },
            "specialeducation": {
                "label": "Special Education",
                "mode": {"teletherapy": 0, "onsite": 2, "home_service": 0},
            },
            "spedtutorials": {
                "label": "SpEd Tutorials",
                "mode": {"teletherapy": 0, "onsite": 2, "home_service": 0},
            },
            "parentcoaching": {
                "label": "Parent Coaching",
                "mode": {"teletherapy": 0, "onsite": 2, "home_service": 0},
            },
            "educationsessionforfamilies": {
                "label": "Education Session for Families",
                "mode": {"teletherapy": 0, "onsite": 2, "home_service": 0},
            },
            "feeding": {
                "label": "Feeding",
                "mode": {"teletherapy": 0, "onsite": 2, "home_service": 0},
            },
            "counseling": {
                "label": "Counseling",
                "mode": {"teletherapy": 0, "onsite": 2, "home_service": 0},
            },
            "psychotherapy": {
                "label": "Psychotherapy",
                "mode": {"teletherapy": 0, "onsite": 1, "home_service": 0},
            },
            "abatherapy": {
                "label": "ABA Therapy",
                "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
            },
            "mnri": {
                "label": "MNRI",
                "mode": {"teletherapy": 0, "onsite": 1, "home_service": 0},
            },
            "sensoryintegration": {
                "label": "Sensory Integration",
                "mode": {"teletherapy": 0, "onsite": 1, "home_service": 0},
            },
            "playschool": {
                "label": "Play School",
                "mode": {"teletherapy": 0, "onsite": 2, "home_service": 0},
            },
            "dysphagiamanagement": {
                "label": "Dysphagia Management",
                "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
            },
            "orthoses": {
                "label": "Orthoses (Splinting)",
                "mode": {"teletherapy": 0, "onsite": 1, "home_service": 0},
            },
            "homeschoolfacilitation": {
                "label": "Homeschool Facilitation",
                "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
            },
            "rehabconsultation": {
                "label": "Rehab Consultation",
                "mode": {"teletherapy": 0, "onsite": 0, "home_service": 0},
            },
        },
    },
}


# def test_create_user():
#     url = "http://localhost:9001/auth/register"
#     data = {
#         "name": "sample name",
#         "email": "sample@sample.com",
#         "password": "mypassword1234",
#         "passwordConfirm": "mypassword1234",
#     }
#     r = requests.post(url, headers={"content-type": "application/json"}, json=data)
#     print(r.text, r.status_code)
#     assert 199 + 1 == 200
#     return r.status_code


def _create_index():
    url = settings.SEARCH_URL + "/facilities_test"
    r = requests.put(url, headers={"content-type": "application/json"})
    return r.status_code, url


def _delete_index():
    url = settings.SEARCH_URL + "/facilities_test"
    r = requests.delete(url, headers={"content-type": "application/json"})
    return r.status_code, url


def test_facilities_endpoint():
    response = client.put("/facilities", data=data)
    assert response.status_code == 401
    pass


def test_facilities_lib():
    _create_index()
    fts = FullTextSearch()
    resp_post = fts.put(
        json.dumps(data),
        settings.SEARCH_URL + f'/facilities_test/_doc/{data["id"]}',
    )
    time.sleep(5)
    resp_get = fts.get(
        {"q": "manila"}, settings.SEARCH_URL + f"/facilities_test/_search"
    )
    assert resp_post["_id"] == str(data["id"])
    _delete_index()
    assert resp_get["hits"]["hits"][0]["_id"] == str(data["id"])
