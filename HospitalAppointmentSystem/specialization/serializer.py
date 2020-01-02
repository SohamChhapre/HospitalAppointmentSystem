from rest_framework.serializers import ModelSerializer
from .models import Specialization

class SpecializationSerializer(ModelSerializer):


    class Meta:
        model = Specialization
        fields = [
            'id',
            'specializations'
        ]


    def to_representation(self, instance):
        ret = super(SpecializationSerializer, self).to_representation(instance)
        ret['name'] = ret.pop('specializations')
        return ret