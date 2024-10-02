from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Banners, Enquiry ,Service,Faq ,Gallery,GalleryImages,SubscriptionPlans,SubscriptionPlansFeatures, SubscriptionType,Trainer,Notify,NotifUserStatus,AssignSubscriber,TrainerAcheivements, TrainerNotification, TrainerSalary

from .forms import EditTrainerPasswordForm, LoginForm,CreateUserForm,EnquiryForms,EditUserProfileForm,TrainerLoginForm,EditTrainerProfileForm,ReportToTrainerForm,ReportToUserForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import CreateView

from django.http import JsonResponse
from django.db.models import Count
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import stripe

from django.views.generic import TemplateView,ListView,CreateView,DetailView,FormView,UpdateView


class HomeView(TemplateView):
    template_name = 'home.html' 

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Add the context data
        context['banners'] = Banners.objects.all()
        context['service'] = Service.objects.all()[:3]
        context['gallery_images'] = GalleryImages.objects.all().order_by('-id')[:8]

        return context


class StaticPageView(TemplateView):
    templates = {
        'about': 'about.html',
        'privacy': 'privacy.html',
        'terms': 'terms.html',
        'contact_us': 'contact_us.html'
    }

    def get_template_names(self):
        # Get the page_name from the URL
        page_name = self.kwargs.get('page_name')
        # Get the template based on page_name
        template_name = self.templates.get(page_name)
        
        if template_name:
            return [template_name]  
   

class FaqPageView(ListView):
    model = Faq 
    template_name = 'faq.html'  
    context_object_name = 'faq'


class EnquiryView(CreateView):
    model = Enquiry  
    form_class = EnquiryForms  
    template_name = 'enquiry.html' 
    success_url = reverse_lazy('enquiry')  # The URL to redirect to after a successful form submission
    
    def form_valid(self, form):
        # Save the form and add a success message
        self.object = form.save()
        messages.success(self.request, "Enquiry has been sent!")  
        return super().form_valid(form)


class GalleryView(ListView):
    model = Gallery  
    template_name = 'gallery.html'  
    context_object_name = 'gallery' 
    ordering = ['-id']  


class GalleryPhotosView(DetailView):
    model = Gallery  # 
    template_name = 'gallery_imgs.html'  
    context_object_name = 'gallery'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all images related to this gallery and order them
        context['gallery_imgs'] = GalleryImages.objects.filter(gallery=self.object).order_by('-id')
        return context
    

class PricingView(View):
    template_name = 'pricing.html'

    def get(self, request, *args, **kwargs):
        # Fetch pricing plans and count registered members
        pricing = SubscriptionPlans.objects.annotate(registered_members=Count('subscriptiontype__id')).all().order_by('price')

        # Retrieve the trainer if the trainer ID exists in the session
        trainer = Trainer.objects.get(pk=request.session['trainerid']) if 'trainerid' in request.session else None
        
        current_plan = None
        is_expired = True  # Default to True, will update if a plan is found

        if request.user.is_authenticated:
            # Logic for authenticated users
            current_plan = SubscriptionType.objects.filter(user=request.user).first()

            if current_plan and current_plan.reg_date and current_plan.plan.validity:
                end_date = current_plan.reg_date + timedelta(days=current_plan.plan.validity)
                is_expired = end_date < datetime.now().date()

        elif trainer:
            current_plan = None  # No plan for trainers
            is_expired = True  

        # Fetch distinct features of subscription plans
        distinct_features = SubscriptionPlansFeatures.objects.all()

        # Prepare context for rendering the template
        context = {
            'pricing': pricing,
            'distinct_features': distinct_features,
            'is_expired': is_expired,
            'current_plan': current_plan
        }

        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class CheckoutView(DetailView):
    model = SubscriptionPlans
    template_name = 'checkout.html'
    context_object_name = 'plan_details'

    def get_object(self):
        # Get the plan by `plan_id` (primary key)
        return SubscriptionPlans.objects.get(pk=self.kwargs['plan_id'])


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

@method_decorator(login_required(login_url='login'), name='dispatch')
class CheckoutSessionView(View):
    def post(self, request, plan_id):
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


@method_decorator(login_required(login_url='login'), name='dispatch')
class PaymentSuccessfulView(View):
    template_name = 'success.html' 

    def get(self, request):

        session_id = request.GET.get('session_id')

        # Retrieve the session using the session ID
        session = stripe.checkout.Session.retrieve(session_id)

        # Get the plan ID from the session
        plan_id = session.client_reference_id

        # Retrieve the corresponding plan
        plan = get_object_or_404(SubscriptionPlans, pk=plan_id)
        user = request.user

        subscription = SubscriptionType.objects.create(
            plan=plan,
            user=user,
            price=plan.price
        )

        context = {
            'plan': plan,
            'subscription_date': subscription.reg_date
        }

        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class PaymentCancelView(View):
    template_name = 'cancel.html'  

    def get(self, request):
        return render(request, self.template_name)


# user functionalities
@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardView(View):
    template_name = 'user/dashboard.html'

    def get(self, request, *args, **kwargs):
        current_plan = None
        current_trainer = None
        social_links = {}
        end_date = None
        achievements = None
        is_expired = True

        # Fetch the current subscription plan
        current_plan = SubscriptionType.objects.filter(user=request.user).first()

        if current_plan:
            # Fetch the current trainer and other related data
            try:
                current_trainer = AssignSubscriber.objects.get(subscriber=current_plan)
                end_date = current_plan.reg_date + timedelta(days=current_plan.plan.validity)
                is_expired = end_date < datetime.now().date()
                social_links = current_trainer.trainer.social_links if current_trainer else {}
                achievements = TrainerAcheivements.objects.filter(trainer=current_trainer.trainer)

            except AssignSubscriber.DoesNotExist:
                current_trainer = None
                social_links = {}

            except TrainerAcheivements.DoesNotExist:
                achievements = None

        # Fetch notifications and unread count
        notifications = Notify.objects.all().order_by('-id')
        total_unread = sum(1 for d in notifications if not NotifUserStatus.objects.filter(user=request.user, notif=d).exists())

        context = {
            'current_plan': current_plan,
            'current_trainer': current_trainer,
            'total_unread': total_unread,
            'end_date': end_date,
            'social_links': social_links,
            'achievements': achievements,
            'is_expired': is_expired
        }

        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateProfileView(View):
    template_name = 'user/edit_profile.html' 


    def get(self, request):
        profile_form = EditUserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
        
        context = {
            'form': profile_form,
            'password_form': password_form,
        }
        
        return render(request, self.template_name, context)


    def post(self, request):
        profile_form = EditUserProfileForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        
        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # Keeps the user logged in after password change
            messages.success(request, "Profile and password updated successfully!")

            return redirect('update_profile')  # Redirect to the same page or a success page
        
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")

            return redirect('update_profile')  
        
        elif password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Password updated successfully!")

            return redirect('update_profile') 

        context = {
            'form': profile_form,
            'password_form': password_form,
        }
        
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class NotificationsView(ListView):
    model = Notify
    template_name = 'notifications.html' 
    context_object_name = 'notifications'  
    ordering = ['-id']  


@method_decorator(login_required(login_url='login'), name='dispatch')
class GetNotificationsView(View):
    def get(self, request, *args, **kwargs):
        notifications = Notify.objects.all().order_by('-id')
        notifStatus = False
        jsonData = []
        total_unread = 0

        for d in notifications:
            try:
                notifStatusData = NotifUserStatus.objects.filter(user=request.user, notif=d).first()

                if notifStatusData:
                    notifStatus = True
                else:
                    notifStatus = False

            except NotifUserStatus.DoesNotExist:
                notifStatus = False

            if not notifStatus:
                total_unread += 1

            jsonData.append({
                'pk': d.id,
                'notify_detail': d.notify_detail,
                'notifStatus': notifStatus
            })

        return JsonResponse({'notifications': jsonData, 'total_unread': total_unread})


@method_decorator(login_required(login_url='login'), name='dispatch')
class MarkReadNotificationsView(View):
    def get(self, request, *args, **kwargs):
        notification_id = request.GET.get('notifications')
        notifications = Notify.objects.get(pk=notification_id)
        user = request.user

        NotifUserStatus.objects.create(notif=notifications, user=user, status=True)
        
        return JsonResponse({'bool': True})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ReportToTrainerView(View):
    template_name = 'user/report_to_trainers.html'

    def get(self, request, *args, **kwargs):
        form = ReportToTrainerForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        form = ReportToTrainerForm(request.POST)
        
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.sender_user = user
            new_form.save()
            messages.success(request, 'Report has been sent!')
            return redirect('report_to_trainer')  # Redirect to avoid form re-submission
        
        context = {'form': form}
        return render(request, self.template_name, context)


# for subscriber chat with trainers
@method_decorator(login_required(login_url='login'), name='dispatch')
class SubscriberChatView(View):
    template_name = 'chat.html'

    def get(self, request, *args, **kwargs):
        try:
            # Get the current logged-in user
            subscription = request.user

            # Fetch the subscriber object associated with the user
            subscriber = get_object_or_404(SubscriptionType, user=subscription)

            # Fetch the assignment of the subscriber to a trainer
            assignment = get_object_or_404(AssignSubscriber, subscriber=subscriber)

            # Get the trainer and their username
            trainer = assignment.trainer
            trainer_name = trainer.username

        except (AssignSubscriber.DoesNotExist, SubscriptionType.DoesNotExist):
            subscriber = None
            trainer = None
            trainer_name = None
            assignment = None

        context = {
            'subscriber': subscriber,
            'trainer': trainer,
            'is_trainer': False,
            'subscriber_id': assignment.id if assignment else None,
            'trainer_name': trainer_name,
            'sender': 'You'
        }

        return render(request, self.template_name, context)


# Trainer logic

class TrainerLoginView(View):
    template_name = 'trainer/login.html'

    def get(self, request, *args, **kwargs):
        form = TrainerLoginForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        trainer = Trainer.objects.filter(username=username, password=password).first()

        if trainer:
            request.session['trainer_login'] = True
            request.session['trainerid'] = trainer.id
            return redirect('trainer_dashboard') 
        else:
            messages.error(request, 'Invalid username or password!')
            form = TrainerLoginForm()  # Re-render the login form

        context = {'form': form}
        return render(request, self.template_name, context)


class TrainerLogoutView(View):
    def get(self, request, *args, **kwargs):
        # Remove trainer login session
        if 'trainer_login' in request.session:
            del request.session['trainer_login']
        
        messages.success(request, 'Logged out successfully!')
        return redirect('trainer_login')
    

class TrainerDashboardView(TemplateView):
    template_name = 'trainer/dashboard.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch trainer details based on session
        trainer_id = self.request.session.get('trainerid')
        trainer = Trainer.objects.get(pk=trainer_id)

        # Fetch achievements (limit to 3)
        achievements = TrainerAcheivements.objects.filter(trainer=trainer)[:3]
        
        # Add to context
        context['trainer'] = trainer
        context['achievement'] = achievements
        
        return context


class TrainerChangePasswordView(FormView):
    template_name = 'trainer/change_password.html'
    form_class = EditTrainerPasswordForm

    def get_trainer(self):
        trainer_id = self.request.session.get('trainerid')
        return Trainer.objects.get(pk=trainer_id)

    def form_valid(self, form):
        trainer = self.get_trainer()
        old_password = form.cleaned_data['old_password']
        new_password1 = form.cleaned_data['new_password1']
        new_password2 = form.cleaned_data['new_password2']

        # Password validation logic
        if old_password != trainer.password:
            messages.error(self.request, "Old password is incorrect.")
            return self.form_invalid(form)

        elif new_password1 != new_password2:
            messages.error(self.request, "New passwords do not match.")
            return self.form_invalid(form)

        else:
            trainer.password = new_password1
            trainer.save()
            messages.success(self.request, "Password updated successfully!")
            return redirect('trainer_change_password')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = self.get_form()  # Pass the form to the template
        
        return context


class TrainerEditProfileView(View):
    template_name = 'trainer/edit_profile.html'

    def get(self, request, *args, **kwargs):
        # Get the trainer ID from the session
        trainer_id = request.session.get('trainerid')
        trainer = Trainer.objects.get(id=trainer_id)

        # Create a form instance with the trainer's current data
        form = EditTrainerProfileForm(instance=trainer)

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Get the trainer ID from the session
        trainer_id = request.session.get('trainerid')
        trainer = Trainer.objects.get(id=trainer_id)

        # Create a form instance with the POST data and FILES for updating
        form = EditTrainerProfileForm(request.POST, request.FILES, instance=trainer)

        if form.is_valid():
            form.save()
            messages.success(request, 'Changes were saved successfully!')
            return redirect('trainer_edit_profile')  # Redirect after successful form submission
        
        # If the form is invalid, re-render the page with form errors
        return render(request, self.template_name, {'form': form})
    

class TrainerAssignedSubscribersView(ListView):
    model = AssignSubscriber
    template_name = 'trainer/assigned_subscribers.html'
    context_object_name = 'trainer_subscribers'
    ordering = ['-id']

    def get_queryset(self):
        trainer_id = self.request.session.get('trainerid')
        trainer = Trainer.objects.get(pk=trainer_id)
        return AssignSubscriber.objects.filter(trainer=trainer).order_by('-id')
    

class TrainerPaymentsView(ListView):
    model = TrainerSalary
    template_name = 'trainer/payments.html'
    context_object_name = 'trainer_payments'

    def get_queryset(self):
        trainer_id = self.request.session.get('trainerid')
        trainer = Trainer.objects.get(pk=trainer_id)
        return TrainerSalary.objects.filter(trainer=trainer)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trainer_payments = self.get_queryset()
        total_amount = sum(tp.amount for tp in trainer_payments)
        context['total_amount'] = total_amount
        return context


class TrainerNotificationsView(ListView):
    model = TrainerNotification
    template_name = 'trainer/notifications.html'
    context_object_name = 'notifications'
    ordering = ['-id'] 

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_count'] = TrainerNotification.objects.filter(is_read=False).count()
        return context
    

class MarkAllAsReadView(View):
    def post(self, request, *args, **kwargs):
        # Update all unread notifications to read
        TrainerNotification.objects.filter(is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    

# For Trainers chat
class TrainerDefaultChatView(View):

    def get(self, request, *args, **kwargs):
        # Check if the trainer is in session
        trainer_id = request.session.get('trainerid')

        if trainer_id:
            # Get the trainer from the session
            trainer = Trainer.objects.get(pk=trainer_id)

            # Get the first assigned subscriber for the trainer
            first_subscriber = AssignSubscriber.objects.filter(trainer=trainer).first()

            # Redirect to the chat with the first subscriber's ID if exists
            if first_subscriber:
                return redirect('trainer_chat', subscriber_id=first_subscriber.id)
        

class TrainerChatView(View):
    template_name = 'chat.html'

    def get(self, request, subscriber_id, *args, **kwargs):
        if request.session.get('trainerid'):
            # Get trainer using the session ID
            trainer = get_object_or_404(Trainer, pk=request.session['trainerid'])

            # Get all subscribers assigned to the trainer
            subscribers = AssignSubscriber.objects.filter(trainer=trainer)

            # Get the selected subscriber based on the passed subscriber_id
            selected_subscriber = get_object_or_404(AssignSubscriber, pk=subscriber_id)

            context = {
                'subscribers': subscribers,
                'selected_subscriber': selected_subscriber,
                'sender': 'You',
                'is_trainer': True
            }

            return render(request, self.template_name, context)


class ReportToUserView(View):
    template_name = 'trainer/report_to_user.html'
    
    def get(self, request, *args, **kwargs):
        form = ReportToUserForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        trainer = Trainer.objects.get(id=request.session['trainerid'])
        form = ReportToUserForm(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.sender_trainer = trainer
            new_form.save()
            messages.success(request, 'Report has been sent!')
            return redirect('report_to_user')  
        
        context = {'form': form}
        return render(request, self.template_name, context)
    