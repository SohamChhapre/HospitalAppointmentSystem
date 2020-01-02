from django.urls import path,include
from .views import AppointmentAPI,GetPatientAppointment,GetDoctorAppointment
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('',AppointmentAPI.as_view()),
    path('patient/<int:id>',GetPatientAppointment.as_view()),
    path('doctor/<int:id>',GetDoctorAppointment.as_view()),
    # path('list/',AppointmentAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)