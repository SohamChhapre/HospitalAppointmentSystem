from rest_framework.serializers import ModelSerializer
from .models import Designation

class DesignationSerializer(ModelSerializer):

    class Meta:
        model = Designation
        fields = [
            'id',
            'designations'
        ]

    def to_representation(self, instance):
        ret = super(DesignationSerializer, self).to_representation(instance)
        ret['name'] = ret.pop('designations')
        return ret