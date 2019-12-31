from django.urls import path,include
from .views import DepartmentListAPI
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('list/',DepartmentListAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)