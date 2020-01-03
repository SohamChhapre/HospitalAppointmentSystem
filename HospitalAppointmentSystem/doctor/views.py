from django.shortcuts import render
from .models import Doctor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import DoctorSerializer,DoctorListSerializer,GetDoctorSerializer
from hospitaldoctor.serializer import HospitalDoctorSerializer
from hospitaldoctor.models import HospitalDoctor
from hospital.models import Hospital
from .models import Doctor
from documents.models import Documents
import json
# Create your views here.

class ListDoctor(APIView):

    def get(self, request, format=None, id=None):
        request = self.request
        if id is None:
            hd = HospitalDoctor.objects.filter(hospital=self.get_hospital_id(request.user)).values_list('doctor')
            queryset = Doctor.objects.filter(id__in=hd)
            serializer = GetDoctorSerializer(queryset, many=True)
            context = {
                    "message":"Doctor's Data",
                    "status":True,
                    "total_doctor":len(serializer.data),
                    "data":serializer.data
                }
            return Response(context, status=status.HTTP_200_OK)
        else:
            queryset = Doctor.objects.filter(id=id).first()
            serializer = GetDoctorSerializer(queryset, many=False)
            if queryset is not None:
                context = {
                    "message":"Doctor's Data",
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
        dept = payload.pop('department')
        deptdata = {
            'department' : dept['name']
        }
        files = datafile
        desigs = payload.pop('designation').split(',')
        specs = payload.pop('specialization').split(',')
        dob = payload.pop('dob').split('T')
        l=[]
        for spec in specs:
            d={}
            d['specializations']=spec
            l.append(d)
        payload['specializations']=l
        l=[]
        for desig in desigs:
            d={}
            d['designations']=desig
            l.append(d)
        payload['designations']=l
        payload['dob']=dob[0]
        payload['gender']='O'
        serializer = DoctorSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            context = {
                "message":"Doctor Created Successfully",
                "status":True,
                "data":serializer.data
            }
            data2 = {
                'hospital' : self.get_hospital_id(request.user),
                'doctor' :    serializer.data['id'],
            }
            for file in files:
                d={}
                d['documents']=files[file]
                Documents.objects.create(**d,doctor_id=serializer.data['id'])
            hpserializer = HospitalDoctorSerializer(data=data2, context=deptdata)
            if hpserializer.is_valid():
                hpserializer.save()
                context.update({'department':hpserializer.data['dept']})
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context = {
                "message":"Doctor Relation error.",
                "status":False,
                "data":hpserializer.error
                }
                return Response(context,status=status.HTTP_400_BAD_REQUEST)
        context = {
                "message":"Wrong data format!!.",
                "status":False,
                "data":serializer.errors
            }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def get_hospital_id(self, id):
        query = Hospital.objects.filter(User=id)
        hospital_id = query.values_list('id', flat=True)[0]
        return hospital_id

    def get_doctor(self, id, hospitalId):
        try:
            hd = HospitalDoctor.objects.filter(hospital=hospitalId,doctor_id=id)
            if hd:
                return Doctor.objects.get(id=id)
            else:
                return None 
        except Doctor.DoesNotExist:
            return None

    def patch(self, request, id, format=None):
        hospitalId = self.get_hospital_id(request.user)
        payload = json.loads(request.data['payload'])
        datafile = request.data
        del datafile['payload']
        if payload.get('department', -2) is not -2:
            dept = payload.pop('department')
            deptdata = {
                'department' : dept['name']
            }
        files = datafile
        if payload.get('dob', -2) is not -2:
            dob = payload.pop('dob').split('T')
            payload['dob']=dob[0]
        if payload.get('specialization', -2) is not -2:
            specs = payload.pop('specialization').split(',')
            l=[]
            for spec in specs:
                d={}
                d['specializations']=spec
                l.append(d)
            payload['specializations']=l
        if payload.get('designation', -2) is not -2:
            desigs = payload.pop('designation').split(',')
            l=[]
            for desig in desigs:
                d={}
                d['designations']=desig
                l.append(d)
            payload['designations']=l
        query = self.get_doctor(id, hospitalId)
        if query:
            serializer = DoctorSerializer(query, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {
                    "message":"Doctor Successfully edited.",
                    "status":True,
                    "data":serializer.data
                }
                for file in files:
                    d={}
                    d['documents']=files[file]
                    Documents.objects.create(**d,doctor_id=serializer.data['id'])
                return Response(context, status=status.HTTP_201_CREATED)
            context = {
                    "message":"Wrong data format!!.",
                    "status":False,
                    "data":serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        context = {
                "message":"Wrong id to patch data!!.",
                "status":False,
                "data":None
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        hospitalId = self.get_hospital_id(request.user)
        query = self.get_doctor(id, hospitalId)
        if query is None:
            context = {
                "message":"Wrong Doctor Id",
                "status":True,
                "data":None
            }
        data = query.delete()
        context = {
            "message":"Doctor Deleted Successfully",
            "status":True,
            "data":data
        }
        return Response(context,status=status.HTTP_204_NO_CONTENT)


class DoctorListAPI(APIView):

    def get(self, request, format=None):
        hd = HospitalDoctor.objects.filter(hospital=self.get_hospital_id(request.user)).values_list('doctor')
        queryset = Doctor.objects.filter(id__in=hd)
        serializer = DoctorListSerializer(queryset, many=True)
        context = {
                "message":"Doctor List Data",
                "status":True,
                "total_doctor":len(serializer.data),
                "data":serializer.data
            }
        return Response(context, status=status.HTTP_200_OK)

    def get_hospital_id(self, id):
        query = Hospital.objects.filter(User=id)
        hospital_id = query.values_list('id', flat=True)[0]
        return hospital_id