from django.shortcuts import render
from rest_framework.views import APIView
from .models import HospitalDoctor
from .serializer import GetHospitalDoctor
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class GetHospitalDoctorDepartmentListAPI(APIView):


    def get(self, request, format=None):
        query = HospitalDoctor.objects.filter()
        serializer = GetHospitalDoctor(query, many=True)
        context = {
                "message":"Department List Data",
                "status":True,
                "total_department":len(serializer.data),
                "data":serializer.data
            }
        return Response(context, status=status.HTTP_200_OK)

