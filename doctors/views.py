"""
Views for doctor management.

All endpoints require JWT authentication.
- GET (list/detail) — all authenticated users can view all doctors.
- POST/PUT/DELETE — only the creator of the record can modify it.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(APIView):
    """
    GET  /api/doctors/     - Retrieve all doctors.
    POST /api/doctors/     - Add a new doctor (authenticated users only).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(
            {
                "status": "success",
                "message": "Doctor record created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class DoctorDetailView(APIView):
    """
    GET    /api/doctors/<id>/  - Get details of a specific doctor.
    PUT    /api/doctors/<id>/  - Update doctor details (creator only).
    DELETE /api/doctors/<id>/  - Delete a doctor record (creator only).
    """

    permission_classes = [IsAuthenticated]

    def _get_doctor(self, pk):
        """Retrieve doctor by primary key."""
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return None

    def get(self, request, pk):
        doctor = self._get_doctor(pk)
        if doctor is None:
            return Response(
                {
                    "status": "error",
                    "message": "Doctor not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = DoctorSerializer(doctor)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        doctor = self._get_doctor(pk)
        if doctor is None:
            return Response(
                {
                    "status": "error",
                    "message": "Doctor not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        # Only the creator can update
        if doctor.created_by != request.user:
            return Response(
                {
                    "status": "error",
                    "message": "You do not have permission to update this record.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "Doctor record updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        doctor = self._get_doctor(pk)
        if doctor is None:
            return Response(
                {
                    "status": "error",
                    "message": "Doctor not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        # Only the creator can delete
        if doctor.created_by != request.user:
            return Response(
                {
                    "status": "error",
                    "message": "You do not have permission to delete this record.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        doctor.delete()
        return Response(
            {
                "status": "success",
                "message": "Doctor record deleted successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
