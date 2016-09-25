from django.contrib import admin

# Register your models here.
from logistics.models import Trip, Driver, Fleet

admin.site.register([Trip, Driver, Fleet])