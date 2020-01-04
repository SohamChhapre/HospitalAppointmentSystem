from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Appointment
from patient.models import Patient
from patient.serializer import PatientSerializer
from doctor.models import Doctor
from doctor.serializer import GetAppointmentDoctorSerializer
from documents.serializer import DocumentPatientSerializer
import datetime
class AppointmentSerializer(ModelSerializer):

    patient_data = SerializerMethodField()
    doctor_data  = SerializerMethodField()
    document     = DocumentPatientSerializer(source='DocumentAppointmentId', many=True)

    class Meta:
        model = Appointment
        fields = [
            'appointment_id',
            'hospital_patient',
            'hospital_doctor',
            'symptoms',
            'time',
            'status',
            'prescriptions',
            'notes',
            'diagnosis',
            'patient_data',
            'doctor_data',
            'document',
        ]

    def get_patient_data(self, obj):
        queryset = Patient.objects.filter(id=obj.hospital_patient.patient.id).first()
        ser = PatientSerializer(queryset, many=False)
        return ser.data

    def get_doctor_data(self, obj):
        queryset = Doctor.objects.filter(id=obj.hospital_doctor.doctor.id).first()
        ser = GetAppointmentDoctorSerializer(queryset, many=False)
        return ser.data

    def to_representation(self, instance):
        ret = super(AppointmentSerializer, self).to_representation(instance)
        time = ret.pop('time')
        date = datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")
        d={}
        d['date']   = date.strftime('%d-%b-%Y')
        d['time']   = date.strftime("%I:%M %p")
        ret['datetime'] = d
        sym = ret.pop('symptoms')
        sym = sym.split(',')
        ret['symptoms']=sym
        pres = ret.pop('prescriptions',' ')
        pres = pres.split(',')
        ret['prescriptions']=pres
        dia = ret.pop('diagnosis',' ')
        dia = dia.split(',')
        ret['diagnosis']=dia
        return ret
        
class AddAppointmentSerializer(ModelSerializer):

    class Meta:
        model = Appointment
        fields = [
            'appointment_id',
            'hospital_patient',
            'hospital_doctor',
            'symptoms',
            'time',
            'status',
            'prescriptions',
            'notes',
            'diagnosis'
        ]