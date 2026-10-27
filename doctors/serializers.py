"""
Serializers for the Doctor model.

All text inputs are sanitized to strip ALL HTML tags and attributes.
"""

from rest_framework import serializers

from healthcare_backend.sanitizer import sanitize

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor CRUD operations.
    """

    created_by = serializers.ReadOnlyField(source="created_by.email")
    specialization_display = serializers.CharField(
        source="get_specialization_display", read_only=True
    )

    class Meta:
        model = Doctor
        fields = (
            "id",
            "created_by",
            "first_name",
            "last_name",
            "specialization",
            "specialization_display",
            "phone",
            "email",
            "license_number",
            "years_of_experience",
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
        allowed = set("0123456789 -+()")
        if not all(c in allowed for c in cleaned):
            raise serializers.ValidationError(
                "Phone number contains invalid characters."
            )
        return cleaned

    def validate_license_number(self, value):
        cleaned = sanitize(value)
        # Check uniqueness (exclude current instance during updates)
        queryset = Doctor.objects.filter(license_number=cleaned)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                "A doctor with this license number already exists."
            )
        return cleaned

    def validate_years_of_experience(self, value):
        if value < 0 or value > 70:
            raise serializers.ValidationError(
                "Years of experience must be between 0 and 70."
            )
        return value
