"""
URL configuration for doctors app.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.DoctorListCreateView.as_view(), name="doctor-list-create"),
    path("<int:pk>/", views.DoctorDetailView.as_view(), name="doctor-detail"),
]
