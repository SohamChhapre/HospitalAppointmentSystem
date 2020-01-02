from django.shortcuts import render
from .serializer import AppointmentSerializer,AddAppointmentSerializer
from .models import Appointment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from hospitalpatient.models import HospitalPatient
from hospitaldoctor.models import HospitalDoctor
import json
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
            queryset = Appointment.objects.filter(appointment_id=id).first()
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

    def post(self, request, format=None):
        payload = json.loads(request.data['payload'])
        patient = payload.pop('patient')
        doctor  = payload.pop('doctor')
        phone  = payload.pop('phone')
        hdid = HospitalDoctor.objects.get(doctor__id=doctor['id'])
        hpid = HospitalPatient.objects.get(patient__id=patient['id'])
        payload['status']='Booked'
        payload['hospital_patient']=hpid.hospital_patient_id
        payload['hospital_doctor']=hdid.hospital_doctor_id
        serializer = AddAppointmentSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            context = {
                "message":"Appointment Added Successfully",
                "status":True,
                "data":serializer.data
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "message":"Wrong Data Format!!",
                "status":False,
                "data":serializer.errors
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
