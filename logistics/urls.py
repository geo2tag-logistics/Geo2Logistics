from django.conf.urls import *

from logistics.views import home
from logistics.views import addFleet
from logistics.views import driverFleets
from logistics.views import base
from logistics.views import driverProfile
from logistics.views import login
from logistics.views import myFleets
from logistics.views import ownerProfile
from logistics.views import map

urlpatterns = [

    url(r'^addFleet/$', addFleet, name='addFleet'),
    url(r'^base/$', base, name='base'),
    url(r'^driverFleets/$', driverFleets, name='driverFleets'),
    url(r'^driverProfile/$', driverProfile, name='driverProfile'),
    url(r'^login/$', login, name='login'),
    url(r'^myFleets/$', myFleets, name='myFleets'),
    url(r'^ownerProfile/$', ownerProfile, name='ownerProfile'),
    url(r'^map/$', map, name='map'),

    url(r'^', home, name='home'),

]