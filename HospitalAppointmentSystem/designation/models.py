from django.db import models
from globals.models import Logs
from doctor.models import Doctor
# Create your models here.

class Designation(Logs):

    doctor_id       = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    designations    = models.CharField(max_length=255)