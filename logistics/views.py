from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Driver

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from logistics.serializers import UserSerializer, GroupSerializer
# Create your views here.

def addFleet(request):
    return render(request, 'logistics/addFleet.html')

def base(request):
    return render(request, 'logistics/base.html')

def driverFleets(request):
    return render(request, 'logistics/driver-fleets.html')

@login_required
def driverProfile(request):
    return render(request, 'logistics/driver-profile.html')

def get_user_role(count):
    return {
        '1': 'Owner',
        '2': 'Driver'
    }

def registration(request):
    if request.method == "POST":
        if request.POST.get('logout'):
            logout(request)
            return render(request, 'logistics/login.html', {
                'error_login': "Logout success!"
            })
        user_role = request.POST.get('status')
        if user_role == 'Owner':
            username = request.POST.get('username', '')
            password = request.POST.get('pass', '')
            return render(request, 'logistics/register.html')
        return render(request, 'logistics/register.html')
    else:
        return render(request, 'logistics/register.html')

def login_user(request):
    if request.method == "POST":
        if request.POST.get('sign-up'):
            return redirect('/reg/')
        username = request.POST.get('username', '')
        password = request.POST.get('pass', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/base/')
            return render(request, 'logistics/login.html', {
                'error_login': "Your account is disabled!"
            })
        return render(request, 'logistics/login.html', {
            'error_login': "Check your username and password!"
        })
    else:
        return render(request, 'logistics/login.html')

def myFleets(request):
    return render(request, 'logistics/myFleets.html')

def ownerProfile(request):
    return render(request, 'logistics/owner-profile.html')

def map(request):
    return render(request, 'logistics/map.html')

def home(request):
    # return render(request, 'logistics/login.html'),
    return render(request, 'logistics/myFleets.html')


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
