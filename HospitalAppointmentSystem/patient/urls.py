from django.urls import path,include
from .views import ListPatient
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('',ListPatient.as_view()),
    path('<int:id>',ListPatient.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)