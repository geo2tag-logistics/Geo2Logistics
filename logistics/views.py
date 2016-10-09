from django.shortcuts import render

# Create your views here.

def addFleet(request):
    return render(request, 'logistics/addFleet.html')

def base(request):
    return render(request, 'logistics/base.html')

def driverFleets(request):
    return render(request, 'logistics/driver-fleets.html')

def driverProfile(request):
        return render(request, 'logistics/driver-profile.html')

def login(request):
    return render(request, 'logistics/login.html')

def myFleets(request):
    return render(request, 'logistics/myFleets.html')

def ownerProfile(request):
    return render(request, 'logistics/owner-profile.html')

def home(request):
    # return render(request, 'logistics/login.html'),
    return render(request, 'logistics/myFleets.html')