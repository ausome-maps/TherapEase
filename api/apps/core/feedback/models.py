import uuid
from django.db import models
from apps.core.facilities.models import Facilities


class Feedback(models.Model):
    STATUS_CHOICES = (
        ("new", "New"),
        ("in_review", "In Review"),
        ("resolved", "Resolved"),
        ("dismissed", "Dismissed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(
        Facilities, on_delete=models.CASCADE, related_name="feedback"
    )
    email_address = models.EmailField()
    contact_number = models.CharField(max_length=50)
    data_concerns = models.TextField()
    usability_concerns = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    admin_notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Feedback from {self.email_address} about {self.facility.properties.placename}"
