from django.shortcuts import render

# Create your views here.
def home(request):
    # return render(request, 'logistics/login.html'),
    return render(request, 'logistics/driver-fleets.html')

def addFleet(request):
    return render(request, 'logistics/addFleet.html')

def driverFleets(request):
    return render(request, 'logistics/driver-fleets.html')