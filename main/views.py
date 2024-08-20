from django.shortcuts import render
from .models import Banners ,Service,Page,Faq ,Gallery,GalleryImages,SubscriptionPlans,SubscriptionPlansFeatures
from .forms import LoginForm,CreateUserForm,EnquiryForms


from django.urls import reverse_lazy
# from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import CreateView


def home(request):

    banners = Banners.objects.all()
    service = Service.objects.all()[:3]
    gallery_images = GalleryImages.objects.all().order_by('-id')[:8]

    context = {"banners":banners,'service':service,'gallery_images':gallery_images}

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
        form = EnquiryForms(request.POST)

        if(form.is_valid()):
            form.save()
            msg = "Data has been saved successfully!"

    form = EnquiryForms
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


def pricing(request):

    pricing = SubscriptionPlans.objects.all().order_by('price')
    distinct_features = SubscriptionPlansFeatures.objects.all()
    context = {'pricing':pricing,'distinct_features':distinct_features}

    return render(request, 'pricing.html',context)


class RegisterView(CreateView):
    form_class = CreateUserForm
    template_name = "register.html"
    success_url = reverse_lazy('')

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully!")
        return super().form_valid(form)


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('')

    def get_success_url(self):
        return self.success_url
    
    def form_valid(self, form):
        user = authenticate(
            request=self.request,
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid username or password.")
            return self.form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Account logged out!")
        return response


