from django.shortcuts import render
from rest_framework.views import APIView
from .models import DoctorDepartment
from .serializer import GetDoctorDepartmentSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class DoctorDepartmentListAPI(APIView):


    def get(self, request, format=None):
        query = DoctorDepartment.objects.filter()
        serializer = GetDoctorDepartmentSerializer(query, many=True)
        context = {
                "message":"Department List Data",
                "status":True,
                "total_department":len(serializer.data),
                "data":serializer.data
            }
        return Response(context, status=status.HTTP_200_OK)

