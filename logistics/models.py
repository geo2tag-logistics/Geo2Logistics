from django.db import models

# Create your models here.

class Trip(models.Model):
    name = models.CharField(max_length=255)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

class Driver(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    def __str__(self):
        return self.firstName+' '+self.lastName

class Fleet(models.Model):
    name = models.CharField(max_length=255)