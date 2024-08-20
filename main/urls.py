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


]+static(settings.MEDIA_URL,document_root = MEDIA_ROOT)