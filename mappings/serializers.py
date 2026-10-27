"""
Serializers for patient-doctor mappings.
"""

from rest_framework import serializers

from doctors.models import Doctor
from patients.models import Patient

from .models import PatientDoctorMapping


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and reading patient-doctor mappings.
    """

    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source="created_by.email")

    class Meta:
        model = PatientDoctorMapping
        fields = (
            "id",
            "patient",
            "patient_name",
            "doctor",
            "doctor_name",
            "created_by",
            "created_at",
        )
        read_only_fields = ("id", "created_by", "created_at")

    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"

    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.first_name} {obj.doctor.last_name}"

    def validate_patient(self, value):
        """Ensure the patient exists."""
        if not Patient.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("Patient not found.")
        return value

    def validate_doctor(self, value):
        """Ensure the doctor exists."""
        if not Doctor.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("Doctor not found.")
        return value

    def validate(self, attrs):
        """Check for duplicate mapping."""
        patient = attrs.get("patient")
        doctor = attrs.get("doctor")

        if patient and doctor:
            existing = PatientDoctorMapping.objects.filter(
                patient=patient, doctor=doctor
            )
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError(
                    "This doctor is already assigned to this patient."
                )

        return attrs
