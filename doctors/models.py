"""
Doctor model for the healthcare application.

Doctors are created by authenticated users. All users can view
doctors, but only the creator can modify or delete them.
"""

from django.conf import settings
from django.db import models


class Doctor(models.Model):
    """
    Represents a doctor record in the healthcare system.
    """

    SPECIALIZATION_CHOICES = [
        ("general", "General Practitioner"),
        ("cardiology", "Cardiology"),
        ("dermatology", "Dermatology"),
        ("neurology", "Neurology"),
        ("orthopedics", "Orthopedics"),
        ("pediatrics", "Pediatrics"),
        ("psychiatry", "Psychiatry"),
        ("surgery", "Surgery"),
        ("oncology", "Oncology"),
        ("gynecology", "Gynecology"),
        ("urology", "Urology"),
        ("radiology", "Radiology"),
        ("ophthalmology", "Ophthalmology"),
        ("ent", "ENT (Ear, Nose, Throat)"),
        ("other", "Other"),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctors",
        help_text="The user who created this doctor record.",
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, default="")
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["specialization"]),
            models.Index(fields=["last_name", "first_name"]),
        ]

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.get_specialization_display()})"
