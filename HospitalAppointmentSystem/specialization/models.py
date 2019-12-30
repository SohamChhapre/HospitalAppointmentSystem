from django.db import models
from globals.models import Logs
from doctor.models import Doctor
# Create your models here.

class Specialization(Logs):

    doctor              = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='SpecializationDoctorId')
    specializations     = models.CharField(max_length=255)

    def __str__(self):
        return self.specializations