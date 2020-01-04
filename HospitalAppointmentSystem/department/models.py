from django.db import models
from globals.models import Logs
# Create your models here.

class Department(Logs):

    dept_id         = models.AutoField(primary_key=True)
    department      = models.CharField(max_length=255)

    def __str__(self):
        return self.department