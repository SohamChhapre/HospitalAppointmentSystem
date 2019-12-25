from django.db import models
from datetime import datetime

class Logs(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active  = models.BooleanField(default=True)
    is_delete  = models.BooleanField(default=False)

    class Meta:
        abstract = True