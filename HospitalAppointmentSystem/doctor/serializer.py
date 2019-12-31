from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Doctor
from designation.models import Designation
from specialization.models import Specialization
from designation.serializer import DesignationSerializer
from specialization.serializer import SpecializationSerializer
from hospitaldoctor.serializer import GetHospitalDoctor
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
            'blood_group',
            'gender',
            'experience', 
            'profile_picture',
            'designations',
            'specializations'
        ]
        read_only_fields = ['user','profile_picture']
    
    def create(self, validated_data):
        validated_data['user']=None
        designations    = validated_data.pop('DesignationDoctorId')
        specializations = validated_data.pop('SpecializationDoctorId')
        doctor          = Doctor.objects.create(**validated_data)
        for designation in designations:
            Designation.objects.create(**designation, doctor=doctor)
        for specialization in specializations:
            Specialization.objects.create(**specialization, doctor=doctor)
        return doctor
        
    def update(self, instance, validated_data):
        
        instance.dob          = validated_data.get("dob", instance.dob)
        instance.email        = validated_data.get("email", instance.email)
        instance.blood_group  = validated_data.get("blood_group", instance.blood_group)
        instance.experience   = validated_data.get("experience", instance.experience)
        
        designations = validated_data.pop('DesignationDoctorId', None)
        specializations = validated_data.pop('SpecializationDoctorId', None)
        instance.save()
        if designations:
            keep_desg = []
            for designation in designations:
                if "id" in designation.keys():
                    if Designation.objects.filter(id=designation["id"]).exists():
                        c = Designation.objects.get(id=designation["id"])
                        c.save()
                        keep_desg.append(c.id)
                    else:
                        continue
                else:
                    c = Designation.objects.create(**designation, doctor=instance)
                    keep_desg.append(c.id)
            q = Designation.objects.filter(doctor=instance)
            for designation in q:
                if designation.id not in keep_desg:
                    designation.delete()

        if specializations: 
            keep_spec = []
            for specialization in specializations:
                if "id" in specialization.keys():
                    if Specialization.objects.filter(id=specialization["id"]).exists():
                        c = Specialization.objects.get(id=specialization["id"])
                        c.save()
                        keep_spec.append(c.id)
                    else:
                        continue
                else:
                    c = Specialization.objects.create(**specialization, doctor=instance)
                    keep_spec.append(c.id)
            q = Specialization.objects.filter(doctor=instance)
            for specialization in q:
                if specialization.id not in keep_spec:
                    specialization.delete()

        return instance

class DoctorListSerializer(ModelSerializer):
    
    specializations = SpecializationSerializer(source='SpecializationDoctorId', many=True)
    age             = serializers.SerializerMethodField()
    department      = GetHospitalDoctor(source='HospitalDoctorDoctorId', many=True)
    
    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'age',
            'specializations',
            'phone',
            'profile_picture',
            'department'
        ]

    def get_age(self, obj):
        today = date.today()
        born = obj.dob
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def to_representation(self, instance):
        ret = super(DoctorListSerializer, self).to_representation(instance)
        k = ret.pop('department')
        ret.update({'department':k[0]})
        return ret
        
class GetDoctorSerializer(ModelSerializer):

    designations    = DesignationSerializer(source='DesignationDoctorId', many=True)
    specializations = SpecializationSerializer(source='SpecializationDoctorId', many=True)
    department      = GetHospitalDoctor(source='HospitalDoctorDoctorId', many=True)
    
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
            'blood_group',
            'gender',
            'experience', 
            'profile_picture',
            'designations',
            'specializations',
            'department'
        ]
        read_only_fields = ['user','profile_picture']

    def to_representation(self, instance):
        ret = super(GetDoctorSerializer, self).to_representation(instance)
        k = ret.pop('department')
        ret.update({'department':k[0]})
        return ret