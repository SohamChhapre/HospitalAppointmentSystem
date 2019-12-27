from django.contrib import admin
from django.urls import path,include
from .views import ListHospital
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', ListHospital.as_view()),
    path('user/<int:id>', ListHospital.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)