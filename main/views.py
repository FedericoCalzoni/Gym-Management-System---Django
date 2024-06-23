from django.shortcuts import render
from .models import Banners

def home(request):
    banners = Banners.objects.all()

    context = {"banners":banners}

    return render(request, 'home.html',context)
