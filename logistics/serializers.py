from .models import Owner, Fleet, Driver, Trip

from rest_framework import serializers


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


class DriverSerializer(serializers.ModelSerializer):
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
            'auto_manufacturer'
        )
