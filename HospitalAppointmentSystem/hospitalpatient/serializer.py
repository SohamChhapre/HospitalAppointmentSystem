from rest_framework import serializers
from .models import HospitalPatient

class HospitalPatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = HospitalPatient
        fields = ['hospital','patient']