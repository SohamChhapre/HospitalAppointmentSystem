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
# Create your views here.

class ListDoctor(APIView):

    def get(self, request, format=None, id=None):
        request = self.request
        if id is None:
            queryset = Doctor.objects.all()
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
        dept = request.data.pop('department')
        deptdata = {
            'department' : dept[0]
        }
        files = request.data.pop('documents')
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                "message":"Doctor Created.",
                "status":True,
                "data":serializer.data
            }
            data2 = {
                'hospital' : self.get_hospital_id(request.user),
                'doctor' :    serializer.data['id'],
            }
            for file in files:
                d={}
                d['documents']=file
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

    def get_doctor(self, id):
        try:
            return Doctor.objects.get(id=id)
        except company.DoesNotExist:
            raise Http404

    def patch(self, request, id, format=None):
        query = self.get_doctor(id)
        serializer = DoctorSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                "message":"Doctor Successfully edited.",
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
        query = self.get_doctor(id)
        data = query.delete()
        context = {
            "message":"Doctor Deleted Successfully",
            "status":True,
            "data":data
        }
        return Response(context,status=status.HTTP_204_NO_CONTENT)


class DoctorListAPI(APIView):

    def get(self, request, format=None):
        queryset = Doctor.objects.all()
        serializer = DoctorListSerializer(queryset, many=True)
        context = {
                "message":"Doctor List Data",
                "status":True,
                "total_doctor":len(serializer.data),
                "data":serializer.data
            }
        return Response(context, status=status.HTTP_200_OK)

