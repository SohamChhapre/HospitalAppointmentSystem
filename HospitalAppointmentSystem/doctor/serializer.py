from rest_framework.serializers import ModelSerializer,SerializerMethodField
from rest_framework import serializers
from .models import Doctor
from designation.models import Designation
from specialization.models import Specialization
from designation.serializer import DesignationSerializer
from specialization.serializer import SpecializationSerializer
from hospitaldoctor.serializer import GetHospitalDoctor
from documents.serializer import DocumentPatientSerializer
from appointment.models import Appointment
from datetime import date
import datetime

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
        read_only_fields = ['user']
    
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
        
        instance.dob                = validated_data.get("dob", instance.dob)
        instance.email              = validated_data.get("email", instance.email)
        instance.blood_group        = validated_data.get("blood_group", instance.blood_group)
        instance.experience         = validated_data.get("experience", instance.experience)
        instance.profile_picture    = validated_data.get("profile_picture", instance.experience)
        
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
    # documents       = DocumentPatientSerializer(source="DocumentDoctorId", many=True)
    appointment     = SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'age',
            'specializations',
            'phone',
            'profile_picture',
            'department',
            # 'documents',
            'appointment',
        ]

    def get_age(self, obj):
        today = date.today()
        born = obj.dob
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def get_appointment(self, obj):
        app = Appointment.objects.filter(hospital_doctor_id__doctor_id=obj.id).count()
        return app

    def to_representation(self, instance):
        ret = super(DoctorListSerializer, self).to_representation(instance)
        k = ret.pop('department')
        k[0]['id'] = k[0].pop('id')
        k[0]['name'] = k[0].pop('name')
        ret.update({'department':k[0]})
        return ret
    
        
class GetDoctorSerializer(ModelSerializer):
    
    designations    = DesignationSerializer(source='DesignationDoctorId', many=True)
    specializations = SpecializationSerializer(source='SpecializationDoctorId', many=True)
    department      = GetHospitalDoctor(source='HospitalDoctorDoctorId', many=True)
    documents       = DocumentPatientSerializer(source="DocumentDoctorId", many=True)
    age             = SerializerMethodField()
    doj             = SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'dob',
            'email',
            'address',
            'age',
            'phone',
            'city',
            'blood_group',
            'gender',
            'experience', 
            'profile_picture',
            'designations',
            'specializations',
            'department',
            'documents',
            'doj'
        ]
        read_only_fields = ['user','profile_picture']
    
    def get_age(self, obj):
        today = date.today()
        born = obj.dob
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def get_doj(self, obj):
        date = obj.created_at
        return date.strftime('%d-%b-%Y')

    def to_representation(self, instance):
        ret = super(GetDoctorSerializer, self).to_representation(instance)
        k = ret.pop('department')
        k[0]['id'] = k[0].pop('id')
        k[0]['name'] = k[0].pop('name')
        ret.update({'department':k[0]})
        date = datetime.datetime.strptime(ret['dob'],"%Y-%m-%d")
        date = date.strftime('%d-%b-%Y')
        ret['dob']=date
        return ret

class GetAppointmentDoctorSerializer(ModelSerializer):

    department      = GetHospitalDoctor(source='HospitalDoctorDoctorId', many=True)

    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'email',
            'profile_picture',
            'department',
        ]
        read_only_fields = ['user']

    def to_representation(self, instance):
        ret = super(GetAppointmentDoctorSerializer, self).to_representation(instance)
        k = ret.pop('department')
        k[0]['id'] = k[0].pop('id')
        k[0]['name'] = k[0].pop('name')
        ret.update({'department':k[0]})
        return ret
    

class GetDoctorList(ModelSerializer):

    class Meta:
        model = Doctor
        fields = [
            'id',
            'name'
        ]