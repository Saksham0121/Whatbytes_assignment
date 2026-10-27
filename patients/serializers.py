"""
Serializers for the Patient model.

All text inputs are sanitized to strip ALL HTML tags and attributes,
preventing stored XSS attacks. Django ORM handles SQL injection prevention.
"""

from rest_framework import serializers

from healthcare_backend.sanitizer import sanitize

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
        return sanitize(value)

    def validate_last_name(self, value):
        return sanitize(value)

    def validate_phone(self, value):
        cleaned = sanitize(value)
        # Allow digits, spaces, hyphens, plus sign, and parentheses
        allowed = set("0123456789 -+()")
        if not all(c in allowed for c in cleaned):
            raise serializers.ValidationError(
                "Phone number contains invalid characters."
            )
        return cleaned

    def validate_address(self, value):
        return sanitize(value)

    def validate_medical_history(self, value):
        return sanitize(value)

    def validate_gender(self, value):
        valid_choices = [choice[0] for choice in Patient.GENDER_CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"Invalid gender. Choose from: {', '.join(valid_choices)}"
            )
        return value

    def validate_date_of_birth(self, value):
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value
