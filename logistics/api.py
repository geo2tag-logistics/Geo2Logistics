from .models import Fleet, Driver, Owner, DriverStats, Trip, TripStats
from .serializers import FleetSerializer, DriverSerializer
from .forms import SignUpForm, LoginForm, FleetAddForm, FleetInviteDismissForm

from django.contrib.auth.decorators import login_required, user_passes_test
from logistics.permissions import is_driver, is_owner

from rest_framework import permissions, status
from logistics.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model # TODO If used custom user model

class SignUp(APIView):
    def post(self, request):
        print(request.data)
        form = SignUpForm(request.data)
        if form.is_valid():
            try:
                user = User.objects.create_user(username=form.cleaned_data["login"], email=form.cleaned_data["email"], password=form.cleaned_data["password"])
                if(form.cleaned_data["is_driver"]):
                    owner = Owner.objects.create(user=user, first_name=form.cleaned_data["first_name"], last_name=form.cleaned_data["last_name"])
                    user.save()
                    owner.save()
                else:
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
        if request.user.is_anonymous() == False:
            return Response({"status": "error", "errors": ["Already login"]}, status=status.HTTP_409_CONFLICT)
        print(request.data)
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


class FleetList(APIView):
    def get(self, request, format=None):
        current_user = request.user
        print(current_user)
        # TODO 1) check user GROUP 2) get user MODEL 3) filter fleets according to model instance
        fleets = Fleet.objects.all()
        serialized_fleets = FleetSerializer(fleets, many=True)
        return Response(serialized_fleets.data, status=status.HTTP_200_OK)


class DriversByFleet(APIView):
    def get(self, request, fleet_id, format=None):
        # TODO manage permissions
        drivers = Driver.objects.filter(fleets=fleet_id)
        serialized_drivers = DriverSerializer(drivers, many=True)
        return Response(serialized_drivers.data, status=status.HTTP_200_OK)


class FleetView(APIView):
    def post(self, request, format=None):
        current_user = request.user
        print(current_user)
        form = FleetAddForm(request.data)
        # TODO Add Owner from request.user & Access level: owner
        owner = Owner.objects.get(id=2)
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


# class UserAuthorize(APIView):
#     def get(self, request, format=None):
#         serialized_users = UserSerializer(users)
#         return Response(serialized_users.data)
#
#
# class OwnerList(APIView):
#     permission_classes = (
#         permissions.IsAuthenticated,
#         # permissions.IsAuthenticatedOrReadOnly,
#         IsOwnerOrReadOnly,
#     )
#
#     def get(self, request, format=None):
#         owners = Owner.objects.all()
#         serialized_users = OwnerSerializer(owners, many=True)
#         return Response(serialized_users.data)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

#
# class DriverList(APIView):
#     permission_classes = (
#         permissions.IsAuthenticated,
#         # permissions.IsAuthenticatedOrReadOnly,
#     )
#
#     def get(self, request, format=None):
#         drivers = Driver.objects.all()
#         serialized_users = DriverSerializer(drivers, many=True)
#         return Response(serialized_users.data)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class UserList(APIView):
#     def get(self, request, format=None):
#         users = User.objects.all()
#         serialized_users = UserSerializer(users, many=True)
#         return Response(serialized_users.data)
#
#
# class UserDetail(APIView):
#     def get(self, request, user_id, format=None):
#         users = User.objects.filter(id=user_id)
#         serialized_users = UserSerializer(users, many=True)
#         return Response(serialized_users.data)
#
#
# class UserSignUp(generics.CreateAPIView):
#     model = get_user_model()
#     permission_classes = [
#         permissions.AllowAny # Or anon users can't register
#     ]
#     serializer_class = UserSerializer
