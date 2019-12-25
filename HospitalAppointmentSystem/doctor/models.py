from django.db import models
from globals.models import Logs
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Doctor(Logs):
    
    GENDER_CHOICES  = (
        ('M','MALE'),
        ('F','FEMALE'),
        ('O','OTHER')
    )
    
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name            = models.CharField(max_length=255, null=True, unique=True)
    dob             = models.DateField()
    email           = models.EmailField(unique=True, blank=False, null=False)
    address         = models.TextField(max_length=500)
    phone           = models.CharField(max_length=12)
    city            = models.CharField(max_length=50)
    gender          = models.CharField(max_length=1,choices=GENDER_CHOICES)
    experience      = models.IntegerField()   
    profile_picture = models.ImageField(upload_to='profile/')

    def __str__(self):
        return self.email