from django.conf.urls import *

from logistics.views import home
from logistics.views import addFleet
from logistics.views import driverFleets

urlpatterns = [
    url(r'^', home, name='home'),
    url(r'^addFleet/$', addFleet, name='addFleet'),
    url(r'^driverFleets/', driverFleets, name='driverFleets')

]