from django.shortcuts import render
from .serializer import AppointmentSerializer
from .models import Appointment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.

class AppointmentAPI(APIView):

    def get(self, request, format=None, id=None):
        if id is None:
            queryset = Appointment.objects.all()
            serializer = AppointmentSerializer(queryset, many=True)
            context = {
                    "message":"Appointment's Data",
                    "status":True,
                    "total_appointment":len(serializer.data),
                    "data":serializer.data
                }
            return Response(context, status=status.HTTP_200_OK)
        else:
            queryset = Appointment.objects.filter(id=id).first()
            serializer = AppointmentSerializer(queryset, many=False)
            if queryset is not None:
                context = {
                    "message":"Appointment's Data",
                    "status":True,
                    "data":serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                    "message":"Invalid Id to get data",
                    "status":False,
                    "data": None
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

class GetPatientAppointment(APIView):
    
    def get(self, request, id, format=None):
        if id is None:
            context = {
                    "message":"Id not provided",
                    "status":False,
                    "data": None
                }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        queryset = Appointment.objects.filter(hospital_patient_id__patient_id=id)
        serializer = AppointmentSerializer(queryset, many=True)
        if queryset:
            context = {
                "message":"Appointment's Data",
                "status":True,
                "data":serializer.data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "message":"Invalid Id to get data",
                "status":False,
                "data": None
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class GetDoctorAppointment(APIView):

    def get(self, request, id, format=None):
        if id is None:
            context = {
                    "message":"Id not provided",
                    "status":False,
                    "data": None
                }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        queryset = Appointment.objects.filter(hospital_doctor_id__doctor_id=id)
        serializer = AppointmentSerializer(queryset, many=True)
        if queryset:
            context = {
                "message":"Appointment's Data",
                "status":True,
                "data":serializer.data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "message":"Invalid Id to get data",
                "status":False,
                "data": None
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
