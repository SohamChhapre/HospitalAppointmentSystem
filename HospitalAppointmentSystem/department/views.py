from django.shortcuts import render
from rest_framework.views import APIView
from .models import Department
from .serializer import DepartmentSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class DepartmentListAPI(APIView):


    def get(self, request, format=None):
        query = Department.objects.all()
        serializer = DepartmentSerializer(query, many=True)
        context = {
                "message":"Department List Data",
                "status":True,
                "total_department":len(serializer.data),
                "data":serializer.data
            }
        return Response(context, status=status.HTTP_200_OK)

