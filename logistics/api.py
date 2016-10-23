from .models import Fleet, Driver
from .serializers import FleetSerializer, DriverSerializer

from rest_framework.views import APIView
from rest_framework.response import Response


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
