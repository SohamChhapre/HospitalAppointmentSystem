from django.db import models
from globals.models import Logs
from hospital.models import Hospital
from patient.models import Patient
# Create your models here.

class HospitalPatient(Logs):

    hospital_patient_id = models.AutoField(primary_key=True)
    hospital         = models.ForeignKey(Hospital,on_delete=models.CASCADE,related_name='hospitalId')
    patient          = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='patientId')


    def __str__(self):
        return "Hospital {} patient {}".format(self.hospital, self.patient)
