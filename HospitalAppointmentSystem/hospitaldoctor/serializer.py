from rest_framework.serializers import ModelSerializer
from .models import HospitalDoctor

class HospitalDoctorSerializer(ModelSerializer):

    class Meta:
        model = HospitalDoctor
        fields = '__all__'