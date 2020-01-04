from django.urls import path,include
from .views import ListDoctor,DoctorListAPI
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('',ListDoctor.as_view()),
    path('<int:id>',ListDoctor.as_view()),
    path('list/',DoctorListAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)