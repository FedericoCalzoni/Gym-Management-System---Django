from django.shortcuts import redirect, render
from .models import Banners ,Service,Page,Faq ,Gallery,GalleryImages,SubscriptionPlans,SubscriptionPlansFeatures, SubscriptionType,Trainer
from .forms import LoginForm,CreateUserForm,EnquiryForms,EditUserProfileForm,TrainerLoginForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import CreateView

import stripe

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


def checkout(request,plan_id):
    planDetails = SubscriptionPlans.objects.get(pk = plan_id)
    context = {'plan_details':planDetails}
    
    return render(request, 'checkout.html', context)


class RegisterView(CreateView):
    form_class = CreateUserForm
    template_name = "register.html"
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully!")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard')

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


stripe.api_key = 'sk_test_51Pqd0GRt8gmpf2hudaW3D1PiCofqvFGUZGJ1qSQ4KgNdmDtYyYwvFm4Bnuk5TB2r76Q5283Nwb5zSgwHpVibD3e400rpSqa9oY'
def checkout_session(request, plan_id):
    plan = SubscriptionPlans.objects.get(pk=plan_id)
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': plan.title,  
                },
                'unit_amount': int(plan.price * 100), 
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/Payment-Successfull?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/Payment-Cancel',
        client_reference_id=plan_id
    )
    
    return redirect(session.url, code=303)


def payment_successfull(request):
    session = stripe.checkout.Session.retrieve(request.GET['session_id'])
    plan_id = session.client_reference_id
    plan = SubscriptionPlans.objects.get(pk = plan_id)
    user = request.user

    SubscriptionType.objects.create(
        plan = plan,
        user = user,
        price = plan.price
        )
    
    return render(request, 'success.html')


def payment_cancel(request):
    return render(request, 'cancel.html')


# user functionalities
def dashboard(request):
    return render(request, 'user/dashboard.html')


def update_profile(request):
    if request.method == 'POST':
        profile_form = EditUserProfileForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        
        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # Keeps the user logged in after password change
            messages.success(request, "Profile and password updated successfully!")
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
        elif password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Password updated successfully!")
    else:
        profile_form = EditUserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
    
    context = {
        'form': profile_form,
        'password_form': password_form,
    }
    
    return render(request, 'user/edit_profile.html', context)


def trainer_login(request):

    msg= ''
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        trainer = Trainer.objects.filter(username=username, password=password).count()
        if(trainer >0):
            request.session['trainer_login'] =True
            return redirect('dashboard')

        else:
            messages.error(request,'Invalid username or password!')

    form = TrainerLoginForm
    context = {'form':form,'msg':msg}

    return render(request, 'trainer/login.html',context)


def trainer_logout(request):
    del request.session['trainer_login']
    messages.success(request,'Logged out successfully!')
    return redirect('trainer_login')