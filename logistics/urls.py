from django.conf.urls import *

from logistics import api
from logistics import views

urlpatterns = [

    # PAGES
    url(r'^addFleet/$', views.addFleet, name='addFleet'),
    url(r'^base/$', views.base, name='base'),
    url(r'^driverFleets/$', views.driverFleets, name='driverFleets'),
    url(r'^driverProfile/$', views.driverProfile, name='driverProfile'),
    url(r'^reg/$', views.registration, name='registration'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^myFleets/$', views.ownerFleets, name='ownerFleets'),
    url(r'^fleet/(?P<fleet_id>[-\w]+)/$', views.ownerFleetId, name='ownerFleetId'),
    url(r'^ownerProfile/$', views.ownerProfile, name='ownerProfile'),
    url(r'^map/$', views.map, name='map'),

    # API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/signup/$', api.SignUp.as_view(), name='api-signup'),
    url(r'^api/auth/$', api.Auth.as_view(), name='api-auth'),
    url(r'^api/logout/$', api.Logout.as_view(), name='api-logout'),

    url(r'^api/fleet/$', api.FleetList.as_view(), name='fleet-list'),
    url(r'^api/fleet/add-fleet/$', api.FleetList().as_view(), name='fleet-add'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/$', api.FleetByIdView().as_view(), name='fleet-by-id'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/drivers/$', api.DriversByFleet().as_view(), name='drivers-by-fleet'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/pending_drivers/$', api.PendingDriversByFleet.as_view(), name='fleet-list'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/delete/$', api.FleetByIdView().as_view(), name='fleet-add'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/invite/$', api.FleetInvite().as_view(), name='drivers-by-fleet'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/dismiss/$', api.FleetDismiss().as_view(), name='drivers-by-fleet'),

    # default
    url(r'^', views.home, name='home'),
]