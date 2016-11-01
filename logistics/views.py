from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.decorators import permission_classes

from logistics.permissions import IsOwnerPermission, IsDriverPermission


@permission_classes((IsOwnerPermission, ))
def addFleet(request):
    return render(request, 'logistics/addFleet.html')


def base(request):
    return render(request, 'logistics/base.html')


@permission_classes((IsDriverPermission, ))
def driverFleets(request):
    return render(request, 'logistics/driver-fleets.html')


@permission_classes((IsDriverPermission, ))
def driverProfile(request):
    return render(request, 'logistics/driver-profile.html')


@permission_classes((IsOwnerPermission, ))
def ownerFleets(request):
    return render(request, 'logistics/owner-fleets.html')


@permission_classes((IsOwnerPermission, ))
def ownerFleetId(request, fleet_id):
    return render(request, 'logistics/owner-fleet-id.html', {"fleet_id": fleet_id})


@permission_classes((IsOwnerPermission, ))
def ownerProfile(request):
    return render(request, 'logistics/owner-profile.html')


@permission_classes((IsOwnerPermission, ))
def map(request):
    return render(request, 'logistics/map.html')


def home(request):
    # return render(request, 'logistics/login.html'),
    return render(request, 'logistics/owner-fleets.html')


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