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
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^myFleets/$', views.ownerFleets, name='ownerFleets'),
    url(r'^fleet/(?P<fleet_id>[-\w]+)/$', views.ownerFleetId, name='ownerFleetId'),
    url(r'^ownerProfile/$', views.ownerProfile, name='ownerProfile'),
    url(r'^map/$', views.map, name='map'),

    # API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/signup/$', api.SignUp.as_view(), name='api-signup'),
    url(r'^api/auth/$', api.Auth.as_view(), name='api-auth'),
    url(r'^api/logout/$', api.Logout.as_view(), name='api-logout'),

    # Owner API
    url(r'^api/fleet/add-fleet/$', api.FleetList().as_view(), name='fleet-add'),
    url(r'^api/fleet/$', api.FleetList.as_view(), name='fleet-list'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/drivers/$', api.DriversByFleet().as_view(), name='drivers-by-fleet'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/pending_drivers/$', api.PendingDriversByFleet.as_view(), name='fleet-list'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/delete/$', api.FleetByIdView().as_view(), name='fleet-add'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/invite/$', api.FleetInvite().as_view(), name='drivers-by-fleet'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/dismiss/$', api.FleetDismiss().as_view(), name='drivers-by-fleet'),
    url(r'^api/fleet/(?P<fleet_id>[-\w]+)/$', api.FleetByIdView().as_view(), name='fleet-by-id'),

    # Driver API
    url(r'^api/driver/pending_fleets/$', api.DriverPendingFleets.as_view(), name='driver-pending-fleets'),
    url(r'^api/driver/pending_fleets/accept/$', api.DriverPendingFleetsAccept.as_view(), name='driver-pf-accept'),
    url(r'^api/driver/pending_fleets/decline/$', api.DriverPendingFleetsDecline.as_view(), name='driver-pf-decline'),
    url(r'^api/driver/fleets/$', api.DriverFleets.as_view(), name='driver-fleets'),
    url(r'^api/driver/fleet/(?P<fleet_id>[-\w]+)/available_trips/$', api.DriverFleetAvailableTrips.as_view(), name='driver-fleet-available-trips'),
    url(r'^api/driver/available_trips/$', api.DriverAvailableTrips.as_view(), name='driver-available-trips'),
    url(r'^api/driver/fleet/(?P<fleet_id>[-\w]+)/trips/$', api.DriverFleetTrips.as_view(), name='driver-fleet-trips'),
    url(r'^api/driver/trips/$', api.DriverTrips.as_view(), name='driver-trips'),
    url(r'^api/driver/accept_trip/(?P<trip_id>[-\w]+)/$', api.DriverAcceptTrip.as_view(), name='driver-accept-trip'),
    url(r'^api/driver/fleet/(?P<fleet_id>[-\w]+)/add_trip/$', api.DriverAddTrip.as_view(), name='driver-add-trip'),
    url(r'^api/driver/current_trip/$', api.DriverCurrentTrip.as_view(), name='driver-current-trip'),
    url(r'^api/driver/report_problem/$', api.DriverReportProblem.as_view(), name='driver-report-problem'),
    url(r'^api/driver/finish_trip/$', api.DriverFinishTrip.as_view(), name='driver-finish-trip'),

    # default
    url(r'^', views.home, name='home'),
]