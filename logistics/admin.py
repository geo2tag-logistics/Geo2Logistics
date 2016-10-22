from django.contrib import admin

# Register your models here.
from logistics.models import Trip, Driver, Fleet, Owner, DriverStats, TripStats

admin.site.register([Trip, Driver, Fleet, Owner, DriverStats, TripStats])