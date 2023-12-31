import uuid
from django.contrib.postgres.fields import ArrayField

from django.db import models


def get_default_services_offered():
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
    return DEFAULT_SERVICES_OFFERED


def get_default_accredition():
    DEFAULT_ACCREDITATION = {"paot": 0, "pasp": 0}
    return DEFAULT_ACCREDITATION


class FacilityProperties(models.Model):
    osm_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    info_src_name = models.CharField(max_length=100, null=True, blank=True, default="")
    info_src_designation = models.CharField(
        max_length=100, null=True, blank=True, default=""
    )
    placename = models.CharField(max_length=250, null=True, blank=True, default="")
    address = models.TextField(null=True, blank=True, default="")
    region = models.CharField(max_length=100, null=True, blank=True, default="")
    city = models.CharField(max_length=100, null=True, blank=True, default="")
    landmarks_desc = models.TextField(null=True, blank=True, default="")
    contact_number = models.CharField(max_length=100, null=True, blank=True, default="")
    alt_contact_number = models.CharField(
        max_length=100, null=True, blank=True, default=""
    )
    email_address = models.CharField(max_length=100, null=True, blank=True, default="")
    website = models.CharField(max_length=100, null=True, blank=True, default="")
    social_media = models.JSONField(blank=True, null=True)
    services_offered = models.JSONField(default=get_default_services_offered)
    other_services = models.JSONField(blank=True, null=True)
    caters_to = ArrayField(
        models.CharField(max_length=100, blank=True, null=True), null=True, blank=True
    )
    images = models.JSONField(blank=True, null=True, default=list)
    accreditation = models.JSONField(default=get_default_accredition)
    status = models.CharField(max_length=10, default="active")

    class Meta:
        verbose_name = "Facility Properties"
        verbose_name_plural = "Facility Properties"
        ordering = ["-osm_id"]


def default_coordinates():
    return {"type": "Point", "coordinates": [0, 0]}


# Create your models here.
class Facilities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    properties = models.OneToOneField(
        FacilityProperties, on_delete=models.CASCADE, related_name="facilities"
    )
    geometry = models.JSONField(null=True, blank=True, default=default_coordinates)

    class Meta:
        verbose_name = "Facilities"
        verbose_name_plural = "Facilities"

    def __str__(self):
        return str(self.properties.placename)
