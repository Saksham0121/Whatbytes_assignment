"""
Views for patient-doctor mapping management.

All endpoints require JWT authentication.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer


class MappingListCreateView(APIView):
    """
    GET  /api/mappings/     - Retrieve all patient-doctor mappings.
    POST /api/mappings/     - Assign a doctor to a patient.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        mappings = PatientDoctorMapping.objects.select_related(
            "patient", "doctor"
        ).all()
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = PatientDoctorMappingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(
            {
                "status": "success",
                "message": "Doctor assigned to patient successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class MappingByPatientView(APIView):
    """
    GET    /api/mappings/<patient_id>/ - Get all doctors assigned to a specific patient.
    DELETE /api/mappings/<id>/         - Remove a doctor from a patient (by mapping ID).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        mappings = PatientDoctorMapping.objects.select_related(
            "patient", "doctor"
        ).filter(patient_id=patient_id)

        if not mappings.exists():
            return Response(
                {
                    "status": "success",
                    "message": "No doctors assigned to this patient.",
                    "data": [],
                },
                status=status.HTTP_200_OK,
            )

        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, patient_id):
        try:
            mapping = PatientDoctorMapping.objects.get(pk=patient_id)
        except PatientDoctorMapping.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "message": "Mapping not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        mapping.delete()
        return Response(
            {
                "status": "success",
                "message": "Doctor removed from patient successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class MappingDeleteView(APIView):
    """
    DELETE /api/mappings/<id>/delete/ - Remove a doctor from a patient.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            mapping = PatientDoctorMapping.objects.get(pk=pk)
        except PatientDoctorMapping.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "message": "Mapping not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        mapping.delete()
        return Response(
            {
                "status": "success",
                "message": "Doctor removed from patient successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
