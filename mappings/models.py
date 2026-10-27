"""
Patient-Doctor mapping model.

Represents the assignment of doctors to patients.
Uses unique_together constraint to prevent duplicate assignments.
"""

from django.conf import settings
from django.db import models

from doctors.models import Doctor
from patients.models import Patient


class PatientDoctorMapping(models.Model):
    """
    Represents a many-to-many relationship between patients and doctors,
    with additional metadata (created_by, timestamps).
    """

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="doctor_mappings",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="patient_mappings",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mappings",
        help_text="The user who created this mapping.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        # Prevent duplicate patient-doctor assignments
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "doctor"],
                name="unique_patient_doctor_mapping",
            )
        ]
        indexes = [
            models.Index(fields=["patient"]),
            models.Index(fields=["doctor"]),
        ]

    def __str__(self):
        return f"{self.patient} → Dr. {self.doctor.first_name} {self.doctor.last_name}"
