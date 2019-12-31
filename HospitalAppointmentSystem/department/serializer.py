from rest_framework.serializers import ModelSerializer
from .models import Department


class DepartmentSerializer(ModelSerializer):

    class Meta:
        model = Department
        fields = ['department','dept_id']

    def create(self, validated_data):
        if Department.objects.filter(department=validated_data['department']).exists():
            dep = Department.objects.get(department=validated_data['department'])
        else:
            dep =  Department.objects.create(**validated_data)
        return dep
