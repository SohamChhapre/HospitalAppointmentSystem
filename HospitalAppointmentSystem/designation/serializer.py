from rest_framework.serializers import ModelSerializer
from .models import Designation

class DesignationSerializer(ModelSerializer):

    class Meta:
        model = Designation
        fields = [
            'id',
            'doctor',
            'designations'
        ]

        read_only_fields = ('doctor',)
