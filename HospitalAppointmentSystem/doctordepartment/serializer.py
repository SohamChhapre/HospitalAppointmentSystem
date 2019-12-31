from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import DoctorDepartment
from department.serializer import DepartmentSerializer

class DoctorDepartmentSerializer(ModelSerializer):
    
    
    class Meta:
        model = DoctorDepartment
        fields = ['hospital_doctor','dept']

class GetDoctorDepartmentSerializer(ModelSerializer):

    dept = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = DoctorDepartment
        fields = ['hospital_doctor','dept']