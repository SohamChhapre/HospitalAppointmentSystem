from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Appointment
from patient.models import Patient
from patient.serializer import PatientSerializer
from doctor.models import Doctor
from doctor.serializer import GetAppointmentDoctorSerializer
from documents.serializer import DocumentPatientSerializer

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

