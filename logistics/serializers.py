from django.contrib.auth.models import Group
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
            'email'
        )


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
