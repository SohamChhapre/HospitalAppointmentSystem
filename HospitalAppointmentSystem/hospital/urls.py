from django.contrib import admin
from django.urls import path,include
from .views import ListHospital,HospitalPatientDoctorAPI
from rest_framework.urlpatterns import format_suffix_patterns
from .dashboard.views import DashboardAPI

urlpatterns = [
    path('', ListHospital.as_view()),
    path('user/<int:id>', ListHospital.as_view()),
    path('details/', HospitalPatientDoctorAPI.as_view()),
    path('dashboard/', DashboardAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)