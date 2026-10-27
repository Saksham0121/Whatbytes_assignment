"""
Serializers for the Patient model.

All text inputs are sanitized using bleach to prevent XSS attacks.
Django ORM's parameterized queries handle SQL injection prevention.
"""

import bleach
from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient CRUD operations.
    Sanitizes all text fields before saving.
    """

    created_by = serializers.ReadOnlyField(source="created_by.email")

    class Meta:
        model = Patient
        fields = (
            "id",
            "created_by",
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "phone",
            "email",
            "address",
            "medical_history",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def validate_first_name(self, value):
        return bleach.clean(value.strip())

    def validate_last_name(self, value):
        return bleach.clean(value.strip())

    def validate_phone(self, value):
        cleaned = bleach.clean(value.strip())
        # Allow digits, spaces, hyphens, plus sign, and parentheses
        allowed = set("0123456789 -+()")
        if not all(c in allowed for c in cleaned):
            raise serializers.ValidationError(
                "Phone number contains invalid characters."
            )
        return cleaned

    def validate_address(self, value):
        return bleach.clean(value.strip())

    def validate_medical_history(self, value):
        return bleach.clean(value.strip())

    def validate_gender(self, value):
        valid_choices = [choice[0] for choice in Patient.GENDER_CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"Invalid gender. Choose from: {', '.join(valid_choices)}"
            )
        return value
