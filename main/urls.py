from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from GYM_MANAGEMENT_SYSTEM.settings import MEDIA_ROOT

from . import views
from .views import CustomLoginView,CustomLogoutView,RegisterView

urlpatterns = [
    path('',views.home,name = ''),
    path('pagedetail/<int:id>',views.page_detail,name = 'page'),    
    path('Faq/',views.faq_page,name = 'faq'),    
    path('Enquiry/',views.enquiry,name = 'enquiry'),    
    path('Gallery/',views.gallery,name = 'gallery'),    
    path('Gallery_Photos<int:id>/',views.gallery_photos,name = 'gallery_photos'),    
    path('Subscription-Plans/',views.pricing,name = 'pricing'),    
    path('Login', CustomLoginView.as_view(),name= 'login'), 
    path('Logout', CustomLogoutView.as_view(),name= 'logout'), 
    path('Register', RegisterView.as_view(),name= 'register'), 
    path('Dashboard', views.dashboard,name= 'dashboard'), 
    path('Edit-Profile', views.update_profile,name= 'update_profile'), 
    path('Plan_Details/<int:plan_id>', views.checkout,name= 'checkout'), 
    path('Checkout/<int:plan_id>', views.checkout_session,name= 'checkout_session'), 
    path('Payment-Successfull', views.payment_successfull,name= 'payment_successfull'), 
    path('Payment-Cancel', views.payment_cancel,name= 'payment_cancel'), 
    path('Trainer-Login', views.trainer_login,name= 'trainer_login'), 
    path('Trainer-Logout', views.trainer_logout,name= 'trainer_logout'), 
    path('Notifications', views.notifications,name= 'notifications'), 


]+static(settings.MEDIA_URL,document_root = MEDIA_ROOT)