from rest_framework import serializers
from .models import Patient
from hospitalpatient.serializer import HospitalPatientDocSerializer
from hospitalpatient.models import HospitalPatient
from appointment.models import Appointment

class PatientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'email',             
            'profile_picture',
        ]

class PatientListSerializer(serializers.ModelSerializer):
    
    documents = HospitalPatientDocSerializer(source='patientId', many=True)
    visits    = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'age',
            'phone',
            'gender',
            'profile_picture',
            'address',
            'city',
            'documents',
            'visits'
        ]

    def to_representation(self, instance):
        ret = super(PatientListSerializer, self).to_representation(instance)
        k = ret.pop('documents')
        ret.update({'documents':k[0].pop('doc')})
        return ret

    def get_visits(self, obj):
        visit = Appointment.objects.filter(hospital_patient_id__patient_id=obj.id).count()
        return visit


class GetPatientSerializer(serializers.ModelSerializer):
    
    documents = HospitalPatientDocSerializer(source='patientId', many=True)
    visits    = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(GetPatientSerializer, self).to_representation(instance)
        k = ret.pop('documents')
        ret.update({'documents':k[0].pop('doc')})
        return ret

    def get_visits(self, obj):
        visit = Appointment.objects.filter(hospital_patient_id__patient_id=obj.id).count()
        return visit

class GetPatientList(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
        ]