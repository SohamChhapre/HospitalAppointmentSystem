from rest_framework.serializers import ModelSerializer
from .models import Specialization

class SpecializationSerializer(ModelSerializer):


    class Meta:
        model = Specialization
        fields = [
            'id',
            'doctor',
            'specializations'
        ]

        read_only_fields = ('doctor',)