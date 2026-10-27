"""
URL configuration for mappings app.

Note: The assignment spec uses:
  - GET /api/mappings/<patient_id>/  to get doctors for a patient
  - DELETE /api/mappings/<id>/       to remove a mapping

To avoid URL pattern conflicts (both take an int), the delete
endpoint uses /api/mappings/<id>/delete/.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.MappingListCreateView.as_view(), name="mapping-list-create"),
    path(
        "<int:patient_id>/",
        views.MappingByPatientView.as_view(),
        name="mapping-by-patient",
    ),
    path(
        "<int:pk>/delete/",
        views.MappingDeleteView.as_view(),
        name="mapping-delete",
    ),
]
