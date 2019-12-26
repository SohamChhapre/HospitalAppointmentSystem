from django.db import models
from globals.models import Logs
from hospitalpatient.models import HospitalPatient
from doctor.models import Doctor
from appointment.models import Appointment

# Create your models here.

class Documents(Logs):
    
    document_id         = models.AutoField(primary_key=True)
    hospital_patient_id = models.ForeignKey(HospitalPatient, related_name='DocumentPatientId', null=True, blank=True, on_delete=models.CASCADE)
    doctor_id           = models.ForeignKey(Doctor, related_name='DocumentDoctorId', null=True, blank=True, on_delete=models.CASCADE)
    appointment_id      = models.ForeignKey(Appointment, related_name='DocumentAppointmentId', null=True, blank=True, on_delete=models.CASCADE)
    documents           = models.FileField(upload_to='docs/')
