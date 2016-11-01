from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from logistics.permissions import is_driver, is_owner, IsOwnerPermission, IsOwnerOrDriverPermission
from .forms import ROLE_CHOICES, SignUpForm, LoginForm, FleetAddForm, FleetInviteDismissForm
from .models import Fleet, Driver, Owner, DriverStats
from .serializers import FleetSerializer, DriverSerializer


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


class FleetView(APIView):
    permission_classes = (IsOwnerPermission,)
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

    def delete(self, request, fleet_id, format=None):
        current_user = request.user
        print(current_user)
        fleet_for_delete = Fleet.objects.get(id=fleet_id)
        # TODO Check owner
        owner = Owner.objects.get(id=fleet_for_delete.owner.id)
        if owner == fleet_for_delete.owner:
            fleet_for_delete.delete()
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)


class FleetInvite(APIView):
    def post(self, request, fleet_id, format=None):
        current_user = request.user
        print(current_user)
        form_invite = FleetInviteDismissForm(request.data)
        print(form_invite)
        if form_invite.is_valid():
            try:
                # TODO If many drivers_id in request
                fleet = Fleet.objects.get(id=fleet_id)
                id = form_invite.cleaned_data.get('driver_id')
                driver = Driver.objects.get(id=id)
                driver.fleets.add(fleet)
                driver.save()
                print(fleet.id, id, driver.id)
                return Response({"status": "ok"}, status=status.HTTP_200_OK)
            except:
                return Response({"status": "error"}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"status": "error2"}, status=status.HTTP_400_BAD_REQUEST)


class FleetDismiss(APIView):
    def post(self, request, fleet_id, format=None):
        current_user = request.user
        print(current_user)
        form_dismiss = FleetInviteDismissForm(request.data)
        print(form_dismiss)
        if form_dismiss.is_valid():
            try:
                # TODO If many drivers_id in request
                fleet = Fleet.objects.get(id=fleet_id)
                id = form_dismiss.cleaned_data.get('driver_id')
                driver = Driver.objects.get(id=id)
                driver.fleets.remove(fleet)
                driver.save()
                print(fleet.id, id, driver.id)
                return Response({"status": "ok"}, status=status.HTTP_200_OK)
            except:
                return Response({"status": "error"}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"status": "error2"}, status=status.HTTP_400_BAD_REQUEST)