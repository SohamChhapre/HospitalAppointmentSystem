from django.db import models
from globals.models import Logs
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Patient(Logs):

    BLOOD_GROUP_CHOICES = (
        ('O-','O-'),
        ('O+','O+'),
        ('A-','A-'),
        ('A+','A+'),
        ('B-','B-'),
        ('B+','B+'),
        ('AB-','AB-'),
        ('AB+','AB+'),
    )

    GENDER_CHOICES  = (
        ('M','MALE'),
        ('F','FEMALE'),
        ('O','OTHER')
    )
    
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    name            = models.CharField(max_length=255, null=True, blank=True)
    age             = models.PositiveSmallIntegerField( null=True, blank=True)
    email           = models.EmailField(unique=True, blank=False, null=False)
    address         = models.TextField(max_length=500, null=True, blank=True)
    blood_group     = models.CharField(max_length=3,choices=BLOOD_GROUP_CHOICES)
    phone           = models.CharField(max_length=12, null=True, blank=True)
    city            = models.CharField(max_length=50, null=True, blank=True)
    gender          = models.CharField(max_length=1,choices=GENDER_CHOICES)
    profile_picture = models.ImageField(upload_to='profile/', null=True, blank=True)

    def __str__(self):
        return self.email
