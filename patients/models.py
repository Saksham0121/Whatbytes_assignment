"""
Patient model for the healthcare application.

Each patient belongs to a specific user (the one who created the record).
This ensures data isolation — users can only see their own patients.
"""

from django.conf import settings
from django.db import models


class Patient(models.Model):
    """
    Represents a patient record in the healthcare system.
    Linked to the user who created it for ownership-based access control.
    """

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patients",
        help_text="The user who created this patient record.",
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, default="")
    address = models.TextField(blank=True, default="")
    medical_history = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_by"]),
            models.Index(fields=["last_name", "first_name"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
