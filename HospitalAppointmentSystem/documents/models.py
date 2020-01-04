from django.db import models
from globals.models import Logs
from hospitalpatient.models import HospitalPatient
from doctor.models import Doctor
from appointment.models import Appointment

# Create your models here.

class Documents(Logs):
    
    document_id         = models.AutoField(primary_key=True)
    hospital_patient    = models.ForeignKey(HospitalPatient, related_name='DocumentPatientId', null=True, blank=True, on_delete=models.CASCADE)
    doctor              = models.ForeignKey(Doctor, related_name='DocumentDoctorId', null=True, blank=True, on_delete=models.CASCADE)
    appointment         = models.ForeignKey(Appointment, related_name='DocumentAppointmentId', null=True, blank=True, on_delete=models.CASCADE)
    documents           = models.FileField(upload_to='docs/')

    def __str__(self):
        return " {} document ".format(self.document_id)
