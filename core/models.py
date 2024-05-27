
# Create your models here.
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    founded = models.DateField()

    def __str__(self):
        return self.name
