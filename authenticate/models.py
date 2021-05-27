from django.db import models
from django.utils import timezone



class File(models.Model):
    #name=models.CharField(max_length=200)
    data=models.JSONField()


