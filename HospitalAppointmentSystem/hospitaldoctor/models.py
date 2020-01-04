from django.db import models
from globals.models import Logs
from hospital.models import Hospital
from doctor.models import Doctor
# Create your models here.

class HospitalDoctor(Logs):

    hospital_doctor_id  = models.AutoField(primary_key=True)
    hospital            = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="HospitalDoctorHospitalId") 
    doctor              = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="HospitalDoctorDoctorId") 


    def __str__(self):
        return "Hospital {} doctor {}".format(self.hospital,self.doctor)
