from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from logistics.permissions import is_driver, is_owner, IsOwnerPermission, IsDriverPermission, IsOwnerOrDriverPermission
from .forms import SignUpForm, LoginForm, FleetAddForm, FleetInviteDismissForm
from .models import Fleet, Driver, Owner, DriverStats
from .serializers import FleetSerializer, DriverSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class SignUp(APIView):
    def post(self, request):
        form = SignUpForm(request.data)
        if form.is_valid():
            try:
                user = User.objects.create_user(username=form.cleaned_data["login"], email=form.cleaned_data["email"], password=form.cleaned_data["password"])
                if form.cleaned_data["role"] == "1" :
                    user.groups.add(Group.objects.get_or_create(name='OWNER')[0])
                    owner = Owner.objects.create(user=user, first_name=form.cleaned_data["first_name"], last_name=form.cleaned_data["last_name"])
                    user.save()
                    owner.save()
                else:
                    user.groups.add(Group.objects.get_or_create(name='DRIVER')[0])
                    driver = Driver.objects.create(user=user, first_name=form.cleaned_data["first_name"], last_name=form.cleaned_data["last_name"])
                    driver_stats = DriverStats.objects.create(driver=driver)
                    user.save()
                    driver.save()
                    driver_stats.save()
                return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": "error", "errors": [str(e)]}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"status": "error", "errors": ["Invalid post parameters"]}, status=status.HTTP_400_BAD_REQUEST)


class Auth(APIView):
    def post(self, request):
        if not request.user.is_anonymous():
            return Response({"status": "error", "errors": ["Already login"]}, status=status.HTTP_409_CONFLICT)
        form = LoginForm(request.data)
        if form.is_valid():
            try:
                user = authenticate(username=form.cleaned_data["login"], password=form.cleaned_data["password"])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return Response({"status": "ok"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status": "error"}, status=status.HTTP_409_CONFLICT)
            except Exception as e:
                return Response({"status": "error", "errors": [str(e)]}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"status": "error", "errors": ["Invalid post parameters"]}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def get(self, request):
        if request.user.is_anonymous():
            return Response({"status": "error", "errors": ["Not authorized"]}, status=status.HTTP_409_CONFLICT)
        else:
            logout(request)
            return Response({"status": "ok"}, status=status.HTTP_200_OK)


class FleetList(APIView):
    permission_classes = (IsOwnerOrDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        if is_owner(request.user):
            fleets = Fleet.objects.filter(owner=request.user.owner)
            serialized_fleets = FleetSerializer(fleets, many=True)
            return Response(serialized_fleets.data, status=status.HTTP_200_OK)
        elif is_driver(request.user):
            fleets = request.user.driver.fleets
            serialized_fleets = FleetSerializer(fleets, many=True)
            return Response(serialized_fleets.data, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "errors": ["Not authorized"]}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        current_user = request.user
        print(current_user)
        form = FleetAddForm(request.data)
        owner = request.user.owner
        if form.is_valid():
            try:
                fleet = form.save(commit=False)
                fleet.owner = owner
                fleet.save()
                print(fleet.name, fleet.description, fleet.owner, fleet.id)
                return Response({"status": "ok", "fleet_id": fleet.id}, status=status.HTTP_201_CREATED)
            except:
                return Response({"status": "error"}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)


class DriversByFleet(APIView):
    permission_classes = (IsOwnerPermission,)

    def get(self, request, fleet_id):
        if Fleet.objects.get(pk=fleet_id) in Fleet.objects.filter(owner=request.user.owner):
            drivers = Driver.objects.filter(fleets=fleet_id)
            serialized_drivers = DriverSerializer(drivers, many=True)
            return Response(serialized_drivers.data, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "errors": ["Wrong fleet_id"]}, status=status.HTTP_409_CONFLICT)


class PendingDriversByFleet(APIView):
    permission_classes = (IsOwnerPermission,)

    def get(self, request, fleet_id):
        if Fleet.objects.get(pk=fleet_id) in Fleet.objects.filter(owner=request.user.owner):
            drivers = Driver.objects.exclude(fleets=fleet_id).exclude(pending_fleets=fleet_id)
            serialized_drivers = DriverSerializer(drivers, many=True)
            return Response(serialized_drivers.data, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "errors": ["Wrong fleet_id"]}, status=status.HTTP_409_CONFLICT)


class FleetByIdView(APIView):
    permission_classes = (IsOwnerPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, fleet_id):
        fleet = Fleet.objects.get(id=fleet_id)
        if fleet in Fleet.objects.filter(owner=request.user.owner):
            serialized_fleet = FleetSerializer(fleet, many=False)
            return Response(serialized_fleet.data, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, fleet_id):
        fleet_for_delete = Fleet.objects.get(id=fleet_id)
        if fleet_for_delete in Fleet.objects.filter(owner=request.user.owner):
            fleet_for_delete.delete()
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)


class FleetInvite(APIView):
    permission_classes = (IsOwnerPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, fleet_id):
        form_invite = FleetInviteDismissForm(request.data)
        if form_invite.is_valid():
            try:
                fleet = Fleet.objects.get(id=fleet_id)
                if fleet in Fleet.objects.filter(owner=request.user.owner):
                    ids = form_invite.cleaned_data.get('driver_id')
                    for driver_id in ids.split(sep=','):
                        if driver_id != '':
                            driver = Driver.objects.get(id=driver_id)
                            driver.fleets.add(fleet)
                            driver.save()
                    return Response({"status": "ok"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "errors": ["Not owner of fleet"]}, status=status.HTTP_409_CONFLICT)
            except Exception as e:
                return Response({"status": "error", "errors": [str(e)]}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)


class FleetDismiss(APIView):
    permission_classes = (IsOwnerPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, fleet_id):
        form_dismiss = FleetInviteDismissForm(request.data)
        if form_dismiss.is_valid():
            try:
                fleet = Fleet.objects.get(id=fleet_id)
                if fleet in Fleet.objects.filter(owner=request.user.owner):
                    id = form_dismiss.cleaned_data.get('driver_id')
                    driver = Driver.objects.get(id=id)
                    driver.fleets.remove(fleet)
                    driver.save()
                    print(fleet.id, id, driver.id)
                    return Response({"status": "ok"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "errors": ["Not owner of fleet"]}, status=status.HTTP_409_CONFLICT)
            except:
                return Response({"status": "error"}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)


# DRIVER API
class DriverPendingFleets(APIView):
    permission_classes = (IsDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        #GET /api/driver/pending_fleets/
        pass

    def post(self, request):
        #POST /api/driver/pending_fleets/
        pass


class DriverFleets(APIView):
    permission_classes = (IsDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        #GET /api/driver/fleets/
        pass


class DriverFleetAvailableTrips(APIView):
    permission_classes = (IsDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, fleet_id):
        #GET /api/driver/fleet/<fleet_id>/available_trips/
        pass


class DriverAvailableTrips(APIView):
    permission_classes = (IsDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        #GET /api/driver/available_trips/
        pass


class DriverFleetTrips(APIView):
    permission_classes = (IsDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, fleet_id):
        #GET /api/driver/fleet/<fleet_id>/trips/
        pass


class DriverTrips(APIView):
    permission_classes = (IsDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        #GET /api/driver/trips/
        pass


class DriverAcceptTrip(APIView):
    permission_classes = (IsDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, trip_id):
        #POST /api/driver/accept_trip/<trip_id>/
        pass


class DriverAddTrip(APIView):
    permission_classes = (IsDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, fleet_id):
        #POST /api/driver/fleet/<fleet_id>/add_trip/
        pass


class DriverCurrentTrip(APIView):
    permission_classes = (IsDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        #GET GET /api/driver/current_trip/
        pass


class DriverReportProblem(APIView):
    permission_classes = (IsDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, fleet_id):
        #POST /api/driver/report_problem/
        pass


class DriverFinishTrip(APIView):
    permission_classes = (IsDriverPermission,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, fleet_id):
        #POST /api/driver/finish_trip/
        pass