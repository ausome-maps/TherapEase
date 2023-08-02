
import requests
import json
import time
from fastapi.testclient import TestClient
from app import dependencies
from app.main import app
from app.libs.search.full_text import FullTextSearch

client = TestClient(app)


def _create_index():
    url = dependencies.SEARCH_URL + "/facilities_test"
    r = requests.put(url, headers={"content-type": "application/json"})
    print(r.text)
    return r.status_code, url

def _delete_index():
    url = dependencies.SEARCH_URL + "/facilities_test"
    r = requests.delete(url, headers={"content-type": "application/json"})
    return r.status_code, url


def test_facilities_endpoint():
    data = {
            "id": 250510750, 
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    121.545819,
                    16.682762
                ]
            },
            "properties": {
                "start": "2023-07-05T21:47:19.651+08:00",
                "end": "2023-07-05T22:10:27.501+08:00",
                "info_src_name": "Kristel Joyce O. Cunanan",
                "info_src_designation": "CSP-PASP-Clinic Manager and Speech-Language Pathologist",
                "placename": "Blausome Therapy Center",
                "address": "23 Burgos St., Purok 6, Victory Sur, Santiago City, Isabela",
                "region": "Region II Cagayan Valley",
                "province": "Isabela",
                "city": "Santiago City",
                "contact_number": "09152747225",
                "alt_contact_number": "09056925329",
                "email_address": "blausometherapycenter@gmail.com",
                "social_media": {
                    "facebook": "Yes, Blausome Therapy Center",
                    "instagram": "Yes, @bl.ausome"
                },
                "caters_to": [
                    "Pediatric Population",
                    "Adolescent Population",
                    "Adult Population"
                ],
                "various_services": {
                    "Special Education-On-site": "Group Individual",
                    "Speech Language Pathology-Teletherapy": "Individual Group",
                    "Speech Language Pathology-On-site": "Group Individual",
                    "Dysphagia-On-site": "Individual",
                    "Parent Coaching-Teletherapy": "Individual Group",
                    "Parent Coaching-On-site": "Group Individual",
                    "Life Skills-On-site": "Group Individual",
                    "Speech Language Therapy-On-site": "Group Individual",
                    "Feeding-On-site": "Individual",
                    "Play School-On-site": "Group",
                    "Educational Session for Families-Teletherapy": "Individual",
                    "Educational Session for Families-On-site": "Group",
                    "SPED Tutorials-Teletherapy": "Individual Group",
                    "Counseling-Teletherapy": "Individual",
                    "Counseling-On-site": "Individual",
                    "Social Skills Training-Teletherapy": "Individual",
                    "Social Skills Training-On-site": "Group Individual",
                    "Sensory Integration-On-site": "Group Individual",
                    "Job Coaching-Teletherapy": "Individual Group",
                    "Job Coaching-On-site": "Group Individual",
                    "Integration Program-Teletherapy": "Individual Group",
                    "Integration Program-On-site": "Group Individual",
                    "Occupational Therapy-On-site": "Group Individual"
                },
                "images": [
                    {
                        "img_1": "IMG_3582-22_10_4.jpg",
                        "img_1_url": "https://kc.kobotoolbox.org/media/original?media_file=chamthesleeptalker%2Fattachments%2F447322184eae4590a1aeac4545f79929%2F89b10ba5-e5eb-402b-a5d3-ab7afaf294ef%2FIMG_3582-22_10_4.jpg"
                    },
                    {
                        "img_2": "IMG_3583-22_10_11.jpg",
                        "img_2_url": "https://kc.kobotoolbox.org/media/original?media_file=chamthesleeptalker%2Fattachments%2F447322184eae4590a1aeac4545f79929%2F89b10ba5-e5eb-402b-a5d3-ab7afaf294ef%2FIMG_3583-22_10_11.jpg"
                    },
                    {
                        "img_3": "IMG_3584-22_10_18.jpg",
                        "img_3_url": "https://kc.kobotoolbox.org/media/original?media_file=chamthesleeptalker%2Fattachments%2F447322184eae4590a1aeac4545f79929%2F89b10ba5-e5eb-402b-a5d3-ab7afaf294ef%2FIMG_3584-22_10_18.jpg"
                    }
                ]
            }

        }

    _create_index()
    fts = FullTextSearch()
    resp_post = fts.put(json.dumps(data),  dependencies.SEARCH_URL + f'/facilities_test/_doc/{data["id"]}')
    time.sleep(1)
    resp_get = fts.get({'q': 'santiago'}, dependencies.SEARCH_URL + f'/facilities_test/_search' )
    assert resp_post["_id"] == str(data["id"])
    _delete_index()
    print(resp_get['hits']['hits'])
    assert resp_get['hits']['hits'][0]["_id"] == str(data["id"])
