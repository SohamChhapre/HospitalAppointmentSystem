from django.shortcuts import render
from .models import Patient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import PatientSerializer,PatientListSerializer,GetPatientSerializer
from hospitalpatient.serializer import HospitalPatientSerializer,HospitalPatientDocSerializer
from hospitalpatient.models import HospitalPatient
from hospital.models import Hospital
from .models import Patient
from documents.models import Documents
import json
# Create your views here.

class ListPatient(APIView):

    def get(self, request, format=None, id=None):
        request = self.request
        if id is None:
            hp = HospitalPatient.objects.filter(hospital=self.get_hospital_id(request.user)).values_list('patient')
            queryset = Patient.objects.filter(id__in=hp)
            serializer = GetPatientSerializer(queryset, many=True)
            context = {
                    "message":"Patient's Data",
                    "status":True,
                    "total_patient":len(serializer.data),
                    "data":serializer.data
                }
            return Response(context, status=status.HTTP_200_OK)
        else:
            queryset = Patient.objects.filter(id=id).first()
            serializer = GetPatientSerializer(queryset, many=False)
            if queryset is not None:
                context = {
                    "message":"Patient's Data",
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
        payload['profile_picture'] = request.data['profile_picture']
        datafile = request.data
        del datafile['payload']
        del datafile['profile_picture']
        files = datafile
        serializer = PatientSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            context = {
                "message":"Patient Created.",
                "status":True,
                "data":serializer.data
            }
            data2 = {
                'hospital' : self.get_hospital_id(request.user),
                'patient' :  serializer.data['id']
            }
            hpserializer = HospitalPatientSerializer(data=data2)
            if hpserializer.is_valid():
                hpserializer.save()
                print(hpserializer.data)
                for file in files:
                    d={}
                    d['documents']=files[file]
                    Documents.objects.create(**d,hospital_patient_id=hpserializer.data['hospital_patient_id'])
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context = {
                "message":"Patient Relation error.",
                "status":False,
                "data":hpserializer.error
                }
                return Response(context,status=status.HTTP_400_BAD_REQUEST)
        context = {
                "message":"Wrong data format!!.",
                "status":False,
                "data":serializer.errors
            }
        print(serializer.errors)
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def get_hospital_id(self, id):
        query = Hospital.objects.filter(User=id)
        hospital_id = query.values_list('id', flat=True)[0]
        return hospital_id

    def get_patient(self, id, hospitalId):
        try:
            hd = HospitalPatient.objects.filter(hospital=hospitalId,patient_id=id)
            if hd:
                return Doctor.objects.get(id=id)
            else:
                return None 
        except Patient.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        hospitalId = self.get_hospital_id(request.user)
        query = self.get_patient(id, hospitalId)
        if query is None:
            context = {
                "message":"Wrong Id to patch data!!.",
                "status":False,
                "data":serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        serializer = PatientSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                "message":"Patient Successfully edited.",
                "status":True,
                "data":serializer.data
            }
            return Response(context, status=status.HTTP_201_CREATED)
        context = {
                "message":"Wrong data format!!.",
                "status":False,
                "data":serializer.errors
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        hospitalId = self.get_hospital_id(request.user)
        query = self.get_patient(id, hospitalId)
        if query is None:
            context = {
            "message":"Wrong Patient Id",
            "status":False,
            "data":None
            }
            return Response(context,status=status.HTTP_204_NO_CONTENT)
        data = query.delete()
        context = {
            "message":"Patient Deleted Successfully",
            "status":True,
            "data":data
        }
        return Response(context,status=status.HTTP_204_NO_CONTENT)


class PatientListAPI(APIView):

    def get(self, request, format=None):
        hp = HospitalPatient.objects.filter(hospital=self.get_hospital_id(request.user)).values_list('patient')
        queryset = Patient.objects.filter(id__in=hp)
        serializer = PatientListSerializer(queryset, many=True)
        context = {
                "message":"Patient List Data",
                "status":True,
                "total_patient":len(serializer.data),
                "data":serializer.data
            }
        return Response(context, status=status.HTTP_200_OK)

    def get_hospital_id(self, id):
        query = Hospital.objects.filter(User=id)
        hospital_id = query.values_list('id', flat=True)[0]
        return hospital_id

