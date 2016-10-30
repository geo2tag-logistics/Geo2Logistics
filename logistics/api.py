from .models import Fleet, Driver, Owner
from .serializers import FleetSerializer, DriverSerializer, UserSerializer, OwnerSerializer

from rest_framework import permissions
from logistics.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model # TODO If used custom user model

class FleetList(APIView):
    def get(self, request, format=None):
        fleets = Fleet.objects.all()
        serialized_fleets = FleetSerializer(fleets, many=True)
        return Response(serialized_fleets.data)


class DriversByFleet(APIView):
    def get(self, request, fleet_id, format=None):
        drivers = Driver.objects.filter(fleets=fleet_id)
        serialized_drivers = DriverSerializer(drivers, many=True)
        return Response(serialized_drivers.data)


# class UserAuthorize(APIView):
#     def get(self, request, format=None):
#         serialized_users = UserSerializer(users)
#         return Response(serialized_users.data)
#

class OwnerList(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        # permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def get(self, request, format=None):
        owners = Owner.objects.all()
        serialized_users = OwnerSerializer(owners, many=True)
        return Response(serialized_users.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DriverList(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        # permissions.IsAuthenticatedOrReadOnly,
    )

    def get(self, request, format=None):
        drivers = Driver.objects.all()
        serialized_users = DriverSerializer(drivers, many=True)
        return Response(serialized_users.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data)


class UserDetail(APIView):
    def get(self, request, user_id, format=None):
        users = User.objects.filter(id=user_id)
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data)


class UserSignUp(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer
