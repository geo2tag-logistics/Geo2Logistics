from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework import serializers

from .models import Owner, Fleet, Driver, Trip


class FleetSerializer(serializers.ModelSerializer):
    cars_count = serializers.SerializerMethodField()
    trips_count = serializers.SerializerMethodField()

    class Meta:
        model = Fleet
        fields = (
            'id',
            'name',
            'description',
            'creation_date',
            'cars_count',
            'trips_count'
        )

    def get_cars_count(self, obj):
        drivers = Driver.objects.filter(fleets=obj)
        return drivers.count()

    def get_trips_count(self, obj):
        trips = Trip.objects.filter(fleet=obj)
        return trips.count()


class OwnerSerializer(serializers.ModelSerializer):
    login = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Owner
        fields = (
            'id',
            'first_name',
            'last_name',
            'is_confirmed',
            'login',
            'email'
        )


class DriverSerializer(serializers.ModelSerializer):
    login = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    is_online = serializers.SerializerMethodField()
    current_trip_fleet_id = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = (
            'id',
            'first_name',
            'last_name',
            'is_online',
            'last_seen',
            'auto_back',
            'auto_model',
            'auto_manufacturer',
            'login',
            'email',
            'current_trip_fleet_id'
        )

    def get_is_online(self, obj):
        if obj.last_seen is not None:
            diff = timezone.now() - obj.last_seen
            if diff.seconds < 2 * 60: # two minutes
                return True
        return False

    def get_current_trip_fleet_id(self, obj):
        try:
            trip = Trip.objects.get(driver=obj, is_finished=False)
            return trip.fleet.id
        except:
            return -1


class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = (
            'id',
            'name',
            'description',
            'passenger_phone',
            'passenger_name',
            'start_position',
            'end_position',
            'start_date',
            'end_date',
            'is_finished',
            'problem',
            'problem_description'
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )
