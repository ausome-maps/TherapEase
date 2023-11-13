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
    info_src_name = models.CharField(max_length=100, null=True, blank=True)
    info_src_designation = models.CharField(max_length=100, null=True, blank=True)
    placename = models.CharField(max_length=250, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    landmarks_desc = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)
    alt_contact_number = models.CharField(max_length=100, null=True, blank=True)
    email_address = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    social_media = models.JSONField(blank=True, null=True)
    services_offered = models.JSONField(default=get_default_services_offered)
    other_services = models.JSONField(blank=True, null=True)
    caters_to = ArrayField(models.CharField(max_length=100, blank=True, null=True))
    images = ArrayField(models.JSONField(blank=True, null=True), null=True, blank=True)
    accreditation = models.JSONField(default=get_default_accredition)

    class Meta:
        verbose_name = "Facility Properties"
        verbose_name_plural = "Facility Properties"


# Create your models here.
class Facilities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    properties = models.ForeignKey(
        FacilityProperties, on_delete=models.CASCADE, related_name="facilities"
    )
    geometry = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Facilities"
        verbose_name_plural = "Facilities"
