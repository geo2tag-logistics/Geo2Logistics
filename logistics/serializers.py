from .models import Owner, Fleet, Driver, Trip
from django.contrib.auth.models import User, Group, Permission

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


class OwnerSerializer(serializers.ModelSerializer):
    #name_of_user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Owner
        fields = (
            'id',
            #'name_of_user',
            'first_name',
            'last_name',
            'is_confirmed',
            #'user'
        )


class DriverSerializer(serializers.ModelSerializer):
    #name_of_user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Driver
        fields = (
            'id',
            #'name_of_user',
            'first_name',
            'last_name',
            'is_online',
            'last_seen',
            'auto_back',
            'auto_model',
            'auto_manufacturer'
        )

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     username = serializers.CharField(max_length=50)
#     email = serializers.EmailField()
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')
#         read_only_fields = ('account_name',)
#
#
# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     permissions = serializers.ManySlugRelatedField(
#         slug_field='codename',
#         queryset=Permission.objects.all()
#     )
#
#     class Meta:
#         model = Group
#         fields = ('url', 'name', 'permissions')

# ROLE_CHOICES = {
#     'OWNER': Owner.objects.all(),
#     'DRIVER': Driver.objects.all(),
# }
#
# # TODO CHECK Рабочий вариант.
# class UserSerializer(serializers.ModelSerializer):
#     owner = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Owner.objects.all(),
#     )
#     driver = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Driver.objects.all()
#     )
#
#     class Meta:
#         model = User
#         fields = (
#             'pk',
#             'id',
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#             'groups',
#             'user_permissions',
#             'is_staff',
#             'is_active',
#             'is_superuser',
#             'last_login',
#             'date_joined',
#             'owner',
#             'driver'
#         )







        # class CreateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = User(
#             email=validated_data['email'],
#             username=validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user