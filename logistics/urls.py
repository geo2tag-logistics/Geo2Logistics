from django.conf.urls import *

from logistics import api

from rest_framework import routers
from logistics import views

urlpatterns = [

    url(r'^addFleet/$', views.addFleet, name='addFleet'),
    url(r'^base/$', views.base, name='base'),
    url(r'^driverFleets/$', views.driverFleets, name='driverFleets'),
    url(r'^driverProfile/$', views.driverProfile, name='driverProfile'),
    url(r'^reg/$', views.registration, name='registration'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^myFleets/$', views.ownerFleets, name='ownerFleets'),
    url(r'^fleet/(?P<fleet_id>[-\w]+)/$', views.ownerFleetId, name='ownerFleetId'),
    url(r'^ownerProfile/$', views.ownerProfile, name='ownerProfile'),
    url(r'^map/$', map, name='map'),

    # API
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/signup/$', api.SignUp.as_view(), name='api-signup'),
    url(r'^api/auth/$', api.Auth.as_view(), name='api-auth'),
    url(r'^api/fleet/$', api.FleetList.as_view(), name='fleet-list'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/drivers/$', api.DriversByFleet().as_view(), name='drivers-by-fleet'),

    # ADMIN API
    # url(r'^api/users/$', api.UserList.as_view(), name='user-list'),
    # url(r'^api/users/(?P<user_id>[-\w]+)/$', api.UserDetail.as_view(), name='users-by-id'),
    # url(r'^api/owners/$', api.OwnerList.as_view(), name='owner-list'),
    # url(r'^api/drivers/$', api.DriverList.as_view(), name='driver-list'),
    # url(r'^api/user_signup/$', api.UserSignUp.as_view(), name='user-signup'),

    # default
    url(r'^', views.home, name='home'),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]