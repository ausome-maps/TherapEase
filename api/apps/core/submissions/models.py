import uuid
from django.db import models
from django.conf import settings
from apps.core.facilities.models import Facilities


class FacilitySubmission(models.Model):
    STATUS_CHOICES = (
        ("new", "New"),
        ("in_review", "In Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("merged", "Merged"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payload = models.JSONField()
    images = models.JSONField(blank=True, default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    admin_notes = models.TextField(blank=True, default="")
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submissions",
    )
    submitter_email = models.EmailField()
    submitter_name = models.CharField(max_length=100, blank=True, default="")
    merged_facility = models.OneToOneField(
        Facilities,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submission",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Facility Submission"
        verbose_name_plural = "Facility Submissions"
        ordering = ["-created_at"]

    def __str__(self):
        placename = ""
        if self.payload and isinstance(self.payload, dict):
            props = self.payload.get("properties", {})
            if isinstance(props, dict):
                placename = props.get("placename", "")
        return f"Submission {self.id} - {placename or 'No placename'}"
