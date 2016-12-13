from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.decorators import permission_classes
from logistics.forms import SignUpForm
from django.contrib.auth.models import User, Group
from .models import Driver, Owner, DriverStats
from logistics.permissions import is_driver, is_owner, IsOwnerPermission, IsDriverPermission, IsOwnerOrDriverPermission


@permission_classes((IsOwnerPermission, ))
def addFleet(request):
    return render(request, 'logistics/addFleet.html')


def base(request):
    if request.user.is_authenticated:
        return render(request, 'logistics/base.html', {'username': request.user.username})
    return render(request, 'logistics/base.html')


@permission_classes((IsOwnerOrDriverPermission, ))
def checkFleets(request):
    if request.user.is_authenticated:
        if is_driver(request.user):
            return redirect('/driverFleets/')
        if is_owner(request.user):
            return redirect('/ownerFleets/')
    return redirect('/login/')


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
    return render(request, 'logistics/owner-fleet-id.html', {"fleet_id": fleet_id, "username": request.user.username})


@permission_classes((IsOwnerPermission, ))
def map(request, fleet_id):
    return render(request, 'logistics/owner-fleet-id-map.html', {"fleet_id": fleet_id, "username": request.user.username})


@permission_classes((IsDriverPermission, ))
def tripId(request, trip_id):
    return render(request, 'logistics/trip-id.html', {"trip_id": trip_id, "username": request.user.username})


@permission_classes((IsOwnerPermission, ))
def ownerProfile(request):
    return render(request, 'logistics/owner-profile.html')


def home(request):
    if request.user.is_authenticated:
        if is_owner(request.user):
            return render(request, 'logistics/owner-fleets.html', {'username': request.user.username})
        if is_driver(request.user):
            return render(request, 'logistics/driver-fleets.html', {'username': request.user.username})
    return render(request, 'logistics/login.html', {'username': request.user.username})


def registration(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data["login"]
            if User.objects.filter(username=login).exists():
                return render(request, 'logistics/register.html', {
                    'error_reg': "Логин уже занят.",
                    'form': form
                })
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                return render(request, 'logistics/register.html', {
                    'error_reg': "Данный e-mail занят.",
                    'form': form
                })
            try:
                user = User.objects.create_user(username=login, email=email,
                                                password=form.cleaned_data["password"])
                if form.cleaned_data["role"] == "1":
                    user.groups.add(Group.objects.get_or_create(name='OWNER')[0])
                    owner = Owner.objects.create(user=user, first_name=form.cleaned_data["first_name"],
                                                 last_name=form.cleaned_data["last_name"])
                    user.save()
                    owner.save()
                else:
                    user.groups.add(Group.objects.get_or_create(name='DRIVER')[0])
                    driver = Driver.objects.create(user=user, first_name=form.cleaned_data["first_name"],
                                                   last_name=form.cleaned_data["last_name"])
                    driver_stats = DriverStats.objects.create(driver=driver)
                    user.save()
                    driver.save()
                    driver_stats.save()
                return render(request, 'logistics/login.html', {
                    'error_login': "Registration success!"
                })
            except Exception as e:
                return render(request, 'logistics/register.html', {
                    'error_reg': e.__str__(),
                    'form': form
                })
        else:
            return render(request, 'logistics/register.html', {
                'error_reg': "Верно заполните данные.",
                'form': form
            })
    else:
        form = SignUpForm()
    return render(request, 'logistics/register.html', {'form': form})


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
                if is_driver(request.user):
                    print("Driver")
                    return redirect('/driverFleets/', {'username': request.user.username})
                if is_owner(request.user):
                    print("Owner")
                    return redirect('/ownerFleets/', {'username': request.user.username})
                return redirect('/base/')
            return render(request, 'logistics/login.html', {
                'error_login': "Your account is disabled!"
            })
        return render(request, 'logistics/login.html', {
            'error_login': "Check your username and password!"
        })
    else:
        return render(request, 'logistics/login.html')


def logout_user(request):
    if request.user.is_anonymous():
        return render(request, 'logistics/login.html', {
            'error_login': "You are not authorized!"
        })
    else:
        logout(request)
        return render(request, 'logistics/login.html', {
            'error_login': "Logout success!"
        })