from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Doctor
from designation.models import Designation
from specialization.models import Specialization
from designation.serializer import DesignationSerializer
from specialization.serializer import SpecializationSerializer
from datetime import date

class DoctorSerializer(ModelSerializer):
    designations    = DesignationSerializer(source='DesignationDoctorId', many=True)
    specializations = SpecializationSerializer(source='SpecializationDoctorId', many=True)

    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'dob',
            'email',
            'address',
            'phone',
            'city',
            'gender',
            'experience', 
            'profile_picture',
            'designations',
            'specializations'
        ]
        read_only_fields = ['user']
    
    def create(self, validated_data):
        # print(validated_data)
        validated_data['user']=None
        designations = validated_data.pop('DesignationDoctorId')
        specializations = validated_data.pop('SpecializationDoctorId')
        doctor = Doctor.objects.create(**validated_data)
        for designation in designations:
            Designation.objects.create(**designation, doctor=doctor)
        for specialization in specializations:
            Specialization.objects.create(**specialization, doctor=doctor)
        return doctor
        
    # def update(self, instance, validated_data):
    #     print(validated_data)

class DoctorListSerializer(ModelSerializer):

    specializations = SpecializationSerializer(source='SpecializationDoctorId', many=True)
    age             = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'age',
            'specializations',
            'phone',
            'profile_picture',
            'dob'
        ]
        # read_only_fields = 'dob'

    def get_age(self, obj):
        today = date.today()
        born = obj.dob
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))