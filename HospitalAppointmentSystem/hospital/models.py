from django.db import models
from globals.models import Logs
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Hospital(Logs):
    User    = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email   = models.EmailField(null=False, blank=False,max_length=255)
    name    = models.CharField(null=False, blank=False,max_length=255)
    address = models.TextField(max_length=500)
    phone   = models.CharField(max_length=12)
    city    = models.CharField(max_length=50)
    logo    = models.ImageField(upload_to='logo/') 


    def __str__(self):
        return self.email