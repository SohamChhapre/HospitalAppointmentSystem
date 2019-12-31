from rest_framework.serializers import ModelSerializer
from .models import HospitalDoctor
from doctordepartment.serializer import DoctorDepartmentSerializer,GetDoctorDepartmentSerializer
from doctordepartment.models import DoctorDepartment
from department.serializer import DepartmentSerializer

class HospitalDoctorSerializer(ModelSerializer):

    class Meta:
        model = HospitalDoctor
        # fields = ['hospital','doctor','hospital_doctor_id']
        fields = '__all__'

    def create(self, validated_data):
        hospitaldoctor = HospitalDoctor.objects.create(**validated_data)
        deptserializer = DepartmentSerializer(data = self.context)
        if deptserializer.is_valid():
            deptserializer.save()
        else:
            print(deptserializer.errors)
        dept = deptserializer.data
        data = {
            'hospital_doctor':hospitaldoctor.hospital_doctor_id,
            'dept':dept['dept_id']
        }
        docdept = DoctorDepartmentSerializer(data=data)
        if docdept.is_valid():
            docdept.save()
        else:
            print(docdept.errors)
        return hospitaldoctor

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        query = DoctorDepartment.objects.filter(hospital_doctor_id=instance.hospital_doctor_id)
        ret.update(query.values('dept')[0])
        return ret


class GetHospitalDoctor(ModelSerializer):

    dept = GetDoctorDepartmentSerializer(source="DoctorDepartmentDoctorId",many=True)
    
    class Meta:
        model = HospitalDoctor
        fields = ['dept','hospital_doctor_id']

    def to_representation(self, instance):
        ret = super(GetHospitalDoctor, self).to_representation(instance)
        ret.pop('hospital_doctor_id')
        k = ret.pop('dept')[0].pop('dept')
        return k