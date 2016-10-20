from django.db import models


class Owner(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)
    #agreement = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.firstName+' '+self.lastName


class Fleet(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField()
    owner = models.ForeignKey(Owner)


class DriverAuto(models.Model):
    back = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    manufacturer = models.CharField(max_length=50, null=True, blank=True)
    #photo = models.ImageField(null=True, blank=True)


class DriverStats(models.Model):
    #TODO not implemented yet
    #текущее местоположение
    nothing = models.IntegerField(null=True, blank=True) #delete


class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    driver_auto = models.OneToOneField(DriverAuto, on_delete=models.CASCADE, null=True, blank=True)
    driver_stats = models.OneToOneField(DriverStats, on_delete=models.CASCADE)
    fleets = models.ManyToManyField(Fleet, related_name="fleets")
    pending_fleets = models.ManyToManyField(Fleet, related_name="pending_fleets")

    def __str__(self):
        return self.firstName+' '+self.lastName


class TripStats(models.Model):
    #TODO not implemented yet
    #длительность
    #дальность
    #маршрут
    nothing = models.IntegerField(null=True, blank=True) #delete

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
    problem = models.IntegerField(choices=PROBLEM,default=1)
    trip_stats = models.OneToOneField(TripStats, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver)
    fleet = models.ForeignKey(Fleet)