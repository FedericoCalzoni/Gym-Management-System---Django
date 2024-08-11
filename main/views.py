from django.shortcuts import render
from .models import Banners ,Service,Page,Faq ,Gallery,GalleryImages
from . import forms


def home(request):

    banners = Banners.objects.all()
    service = Service.objects.all()[:3]
    context = {"banners":banners,'service':service}

    return render(request, 'home.html',context)

def page_detail(request,id):

    pages = Page.objects.get(id=id)
    context = {'pages':pages}

    return render(request, 'page.html',context)


def faq_page(request):

    faq = Faq.objects.all()
    context = {'faq':faq}

    return render(request, 'faq.html',context)


def enquiry(request):

    msg= ''
    if(request.method == 'POST'):
        form = forms.EnquiryForms(request.POST)

        if(form.is_valid()):
            form.save()
            msg = "Data has been saved successfully!"

    form = forms.EnquiryForms
    context = {'form':form,'msg':msg}

    return render(request, 'enquiry.html',context)


def gallery (request):

    gallery = Gallery.objects.all().order_by('-id')
    context = {'gallery':gallery}

    return render(request, 'gallery.html',context)

def gallery_photos(request,id):
    
    gallery = Gallery.objects.get(id=id)
    gallery_imgs = GalleryImages.objects.filter(gallery=gallery).order_by('-id')
    context = {'gallery_imgs':gallery_imgs,'gallery':gallery}

    return render(request, 'gallery_imgs.html',context)

