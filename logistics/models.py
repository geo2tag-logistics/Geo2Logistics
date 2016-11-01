from django.contrib.auth.models import User
from django.db import models


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)
    # agreement = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Fleet(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(Owner)

    def __str__(self):
        return self.name


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    auto_back = models.CharField(max_length=50, null=True, blank=True)
    auto_model = models.CharField(max_length=50, null=True, blank=True)
    auto_manufacturer = models.CharField(max_length=50, null=True, blank=True)
    # auto_photo = models.ImageField(null=True, blank=True)

    fleets = models.ManyToManyField(Fleet, related_name="fleets", blank=True)
    pending_fleets = models.ManyToManyField(Fleet, related_name="pending_fleets", blank=True)

    def __str__(self):
        return self.first_name+' '+self.last_name


class DriverStats(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)
    # TODO текущее местоположение

    def __str__(self):
        return self.driver.first_name+' '+self.driver.last_name+' stats'


class Trip(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    PROBLEM = (
        (1, 'none'),
        (2, 'crash'),
        (3, 'jam'),
        (4, 'other'),
    )
    problem = models.IntegerField(choices=PROBLEM, default=1)

    driver = models.ForeignKey(Driver)
    fleet = models.ForeignKey(Fleet)

    def __str__(self):
        return 'trip ' + self.name


class TripStats(models.Model):
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE)
    # TODO длительность, дальность, маршрут

    def __str__(self):
        return 'Trip ' + self.trip.name + ' stats'
