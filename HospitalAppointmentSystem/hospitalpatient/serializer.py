from rest_framework import serializers
from .models import HospitalPatient
from documents.serializer import DocumentPatientSerializer

class HospitalPatientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HospitalPatient
        fields = ['hospital','patient']

class HospitalPatientDocSerializer(serializers.ModelSerializer):

    doc = DocumentPatientSerializer(source='DocumentPatientId', many=True)

    class Meta:
        model = HospitalPatient
        fields = ['doc']

