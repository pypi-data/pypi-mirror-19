from django.shortcuts import render

# Create your views here.


def deviantart_profile(request):
    return render(request, 'profile.html')
