from django.db import models
from globals.models import Logs
from hospitalpatient.models import HospitalPatient
from hospitaldoctor.models import HospitalDoctor
# Create your models here.

class Appointment(Logs):
    
    STATUS_CHOICES = (
        ('Booked','Booked'),
        ('Canceled','Canceled'),
        ('Visited','Visited')
    )
    
    appointment_id      = models.AutoField(primary_key=True)
    hospital_patient = models.ForeignKey(HospitalPatient, on_delete=models.CASCADE, related_name='AppointmentPatientId')
    hospital_doctor  = models.ForeignKey(HospitalDoctor, on_delete=models.CASCADE, related_name='AppointmentDoctorId')
    symptoms            = models.TextField(max_length=255, blank=True, null=True)
    time                = models.DateTimeField()
    status              = models.CharField(max_length=10,choices=STATUS_CHOICES)
    prescriptions       = models.TextField(max_length=500, blank=True, null=True)
    notes               = models.TextField(max_length=500, blank=True, null=True)
    diagnosis           = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.appointment_id