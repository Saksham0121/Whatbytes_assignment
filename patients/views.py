"""
Views for patient management.

All endpoints require JWT authentication.
Users can only access patients they created (ownership-based access control).
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient
from .serializers import PatientSerializer


class PatientListCreateView(APIView):
    """
    GET  /api/patients/     - Retrieve all patients created by the authenticated user.
    POST /api/patients/     - Add a new patient record.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.filter(created_by=request.user)
        serializer = PatientSerializer(patients, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(
            {
                "status": "success",
                "message": "Patient record created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class PatientDetailView(APIView):
    """
    GET    /api/patients/<id>/  - Get details of a specific patient.
    PUT    /api/patients/<id>/  - Update patient details.
    DELETE /api/patients/<id>/  - Delete a patient record.
    """

    permission_classes = [IsAuthenticated]

    def _get_patient(self, pk, user):
        """Helper to retrieve a patient owned by the requesting user."""
        try:
            return Patient.objects.get(pk=pk, created_by=user)
        except Patient.DoesNotExist:
            return None

    def get(self, request, pk):
        patient = self._get_patient(pk, request.user)
        if patient is None:
            return Response(
                {
                    "status": "error",
                    "message": "Patient not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PatientSerializer(patient)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        patient = self._get_patient(pk, request.user)
        if patient is None:
            return Response(
                {
                    "status": "error",
                    "message": "Patient not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "Patient record updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        patient = self._get_patient(pk, request.user)
        if patient is None:
            return Response(
                {
                    "status": "error",
                    "message": "Patient not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        patient.delete()
        return Response(
            {
                "status": "success",
                "message": "Patient record deleted successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
