from django.db import models
from globals.models import Logs
from doctor.models import Doctor
# Create your models here.

class Specialization(Logs):

    doctor_id           = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    specializations     = models.CharField(max_length=255)