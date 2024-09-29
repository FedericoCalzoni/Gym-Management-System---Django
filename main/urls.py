from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from GYM_MANAGEMENT_SYSTEM.settings import MEDIA_ROOT

from . import views
from .views import CustomLoginView,CustomLogoutView,RegisterView

urlpatterns = [
    path('',views.home,name = ''),   
    path('Faq/',views.faq_page,name = 'faq'),      
    path('Enquiry/',views.enquiry,name = 'enquiry'),    
    path('pages/<str:page_name>/', views.static_pages, name='static_page'),
    path('Gallery/',views.gallery,name = 'gallery'),    
    path('Gallery_Photos<int:id>/',views.gallery_photos,name = 'gallery_photos'),    
    path('Subscription-Plans/',views.pricing,name = 'pricing'),    


    path('Trainer-Default-Chat/',views.trainer_default_chat,name = 'trainer_default_chat'),    
    path('Trainer-Chat/<int:subscriber_id>/',views.trainer_chat,name = 'trainer_chat'),    

    # User
    path('Login', CustomLoginView.as_view(),name= 'login'), 
    path('Logout', CustomLogoutView.as_view(),name= 'logout'), 
    path('Register', RegisterView.as_view(),name= 'register'), 
    path('Dashboard', views.dashboard,name= 'dashboard'), 
    path('Edit-Profile', views.update_profile,name= 'update_profile'), 
    path('Report-To-Trainer', views.report_to_trainer,name= 'report_to_trainer'), 


    path('Subscriber-Chat', views.subscriber_chat,name= 'subscriber_chat'), 
    

    path('Plan_Details/<int:plan_id>', views.checkout,name= 'checkout'), 
    path('Checkout/<int:plan_id>', views.checkout_session,name= 'checkout_session'), 

    #Payment
    path('Payment-Successfull', views.payment_successfull,name= 'payment_successfull'), 
    path('Payment-Cancel', views.payment_cancel,name= 'payment_cancel'), 

    #Trainer
    path('Trainer-Login', views.trainer_login,name= 'trainer_login'), 
    path('Trainer-Dashboard', views.trainer_dashboard,name= 'trainer_dashboard'), 
    path('Trainer-Logout', views.trainer_logout,name= 'trainer_logout'),
    path('Change-Password', views.trainer_change_password,name= 'trainer_change_password'),
    path('Account-Settings', views.trainer_edit_profile,name= 'trainer_edit_profile'),
    path('Assigned-Subscribers', views.trainer_assigned_subscribers,name= 'trainer_assigned_subscribers'),
    path('Payments', views.trainer_payments,name= 'trainer_payments'),
    path('Trainer-Notifications', views.trainer_notifications,name= 'trainer_notifications'),
    path('notifications/mark_all_as_read', views.mark_all_as_read,name= 'mark_all_as_read'),
    path('Messages', views.trainer_messages,name= 'trainer_messages'),
    path('Report-to-user', views.report_to_user,name= 'report_to_user'),
    

    # Notifications
    path('Notifications', views.notifications,name= 'notifications'), 
    path('Get-Notifications', views.get_notifications,name= 'get_notifications'), 
    path('mark_read_notifications', views.mark_read_notifications,name= 'mark_read_notifications'), 


]+static(settings.MEDIA_URL,document_root = MEDIA_ROOT)