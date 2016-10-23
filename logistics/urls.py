from django.conf.urls import *

from logistics import api
from logistics.views import home
from logistics.views import addFleet
from logistics.views import driverFleets
from logistics.views import base
from logistics.views import driverProfile
from logistics.views import login_user
from logistics.views import myFleets
from logistics.views import ownerProfile
from logistics.views import map
from logistics.views import registration

urlpatterns = [

    url(r'^addFleet/$', addFleet, name='addFleet'),
    url(r'^base/$', base, name='base'),
    url(r'^driverFleets/$', driverFleets, name='driverFleets'),
    url(r'^driverProfile/$', driverProfile, name='driverProfile'),
    url(r'^reg/$', registration, name='registration'),
    url(r'^login/$', login_user, name='login'),
    url(r'^myFleets/$', myFleets, name='myFleets'),
    url(r'^ownerProfile/$', ownerProfile, name='ownerProfile'),
    url(r'^map/$', map, name='map'),

    # API
    url(r'^api/fleet/$', api.FleetList.as_view(), name='fleet-list'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/drivers/$', api.DriversByFleet().as_view(), name='drivers-by-fleet'),

    url(r'^', home, name='home'),

]