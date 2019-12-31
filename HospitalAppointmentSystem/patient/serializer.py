from rest_framework import serializers
from .models import Patient
from hospitalpatient.serializer import HospitalPatientDocSerializer

class PatientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Patient
        fields = '__all__'

class PatientListSerializer(serializers.ModelSerializer):
    
    documents = HospitalPatientDocSerializer(source='patientId', many=True)

    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'age',
            'phone',
            'profile_picture',
            'address',
            'city',
            'documents'
        ]

    def to_representation(self, instance):
        ret = super(PatientListSerializer, self).to_representation(instance)
        k = ret.pop('documents')
        # print()
        ret.update({'documents':k[0].pop('doc')})
        return ret

class GetPatientSerializer(serializers.ModelSerializer):
    
    documents = HospitalPatientDocSerializer(source='patientId', many=True)

    class Meta:
        model = Patient
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(GetPatientSerializer, self).to_representation(instance)
        k = ret.pop('documents')
        # print()
        ret.update({'documents':k[0].pop('doc')})
        return ret