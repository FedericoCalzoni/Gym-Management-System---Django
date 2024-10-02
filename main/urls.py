from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from GYM_MANAGEMENT_SYSTEM.settings import MEDIA_ROOT

from .views import *

urlpatterns = [

    # General 
    path('',HomeView.as_view(),name = ''),   
    path('Faq/',FaqPageView.as_view(),name = 'faq'),      
    path('Enquiry/',EnquiryView.as_view(),name = 'enquiry'),    
    path('pages/<str:page_name>/', StaticPageView.as_view(), name='static_page'),
    path('Gallery/',GalleryView.as_view(),name = 'gallery'),    
    path('Gallery_Photos<pk>/',GalleryPhotosView.as_view(),name = 'gallery_photos'),    
    path('Subscription-Plans/',PricingView.as_view(),name = 'pricing'),    
  
    # User
    path('Login', CustomLoginView.as_view(),name= 'login'), 
    path('Logout', CustomLogoutView.as_view(),name= 'logout'), 
    path('Register', RegisterView.as_view(),name= 'register'), 
    path('Dashboard', DashboardView.as_view(),name= 'dashboard'), 
    path('Edit-Profile', UpdateProfileView.as_view(),name= 'update_profile'), 
    path('Report-To-Trainer', ReportToTrainerView.as_view(),name= 'report_to_trainer'), 

    # User chat
    path('Subscriber-Chat', SubscriberChatView.as_view(),name= 'subscriber_chat'), 
    
    # User Notifications
    path('Notifications', NotificationsView.as_view(),name= 'notifications'), 
    path('Get-Notifications',GetNotificationsView.as_view(),name= 'get_notifications'), 
    path('mark_read_notifications', MarkReadNotificationsView.as_view(),name= 'mark_read_notifications'), 

    # Pricing Plans
    path('Plan_Details/<int:plan_id>', CheckoutView.as_view(),name= 'checkout'), 
    path('Checkout/<int:plan_id>', CheckoutSessionView.as_view(),name= 'checkout_session'), 

    # Stripe Payment
    path('Payment-Successfull', PaymentSuccessfulView.as_view(),name= 'payment_successfull'), 
    path('Payment-Cancel', PaymentCancelView.as_view(),name= 'payment_cancel'), 

    # Trainer
    path('Trainer-Login', TrainerLoginView.as_view(),name= 'trainer_login'), 
    path('Trainer-Dashboard', TrainerDashboardView.as_view(),name= 'trainer_dashboard'), 
    path('Trainer-Logout', TrainerLogoutView.as_view(),name= 'trainer_logout'),
    path('Change-Password', TrainerChangePasswordView.as_view(),name= 'trainer_change_password'),
    path('Account-Settings', TrainerEditProfileView.as_view(),name= 'trainer_edit_profile'),
    path('Assigned-Subscribers', TrainerAssignedSubscribersView.as_view(),name= 'trainer_assigned_subscribers'),
    path('Payments', TrainerPaymentsView.as_view(),name= 'trainer_payments'),
    path('Report-to-user', ReportToUserView.as_view(),name= 'report_to_user'),

    # Trainer notifications
    path('Trainer-Notifications', TrainerNotificationsView.as_view(),name= 'trainer_notifications'),
    path('notifications/mark_all_as_read', MarkAllAsReadView.as_view(),name= 'mark_all_as_read'),

    # Trainer Chat
    path('Trainer-Default-Chat/',TrainerDefaultChatView.as_view(),name = 'trainer_default_chat'),     
    path('Trainer-Chat/<int:subscriber_id>/',TrainerChatView.as_view(),name = 'trainer_chat'),  
    


]+static(settings.MEDIA_URL,document_root = MEDIA_ROOT)