from django.shortcuts import render
from .models import Banners ,Service

def home(request):
    banners = Banners.objects.all()
    service = Service.objects.all()[:3]

    context = {"banners":banners,'service':service}

    return render(request, 'home.html',context)
