from django.shortcuts import render
from .models import Hospital
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import HospitalSerializer
from patient.serializer import GetPatientList
from patient.models import Patient
from doctor.serializer import GetDoctorList
from doctor.models import Doctor
# Create your views here.

class ListHospital(APIView):


    def get(self, request, format=None, id=None):
        request = self.request
        if id is None:
            queryset = Hospital.objects.all()
            serializer = HospitalSerializer(queryset, many=True)
            context = {
                    "message":"Hospital's Data",
                    "status":True,
                    "data":serializer.data
                }
            return Response(context, status=status.HTTP_200_OK)
        else:
            queryset = Hospital.objects.filter(User=id).first()
            serializer = HospitalSerializer(queryset, many=False)
            if queryset is not None:
                context = {
                    "message":"Hospital's Data",
                    "status":True,
                    "data":serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                    "message":"Invalid User Id to get data",
                    "status":False,
                    "data": None
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, format=None):
        query = self.get_hospital(id)
        serializer = HospitalSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HospitalPatientDoctorAPI(APIView):

    def get(self, request, format=None):
        queryset = Patient.objects.all()
        serializer = GetPatientList(queryset, many=True)
        data = {}
        data['patient'] = serializer.data
        queryset = Doctor.objects.all()
        serializer = GetDoctorList(queryset, many=True)
        data['doctor'] = serializer.data
        context = {
            "message": "Hospital Doctor And Patient",
            "status": True,
            "data":data
        }
        return Response(context, status=status.HTTP_200_OK)