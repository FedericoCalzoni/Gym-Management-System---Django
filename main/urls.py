from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from GYM_MANAGEMENT_SYSTEM.settings import MEDIA_ROOT

from . import views

urlpatterns = [
    path('',views.home,name = '')
]+static(settings.MEDIA_URL,document_root = MEDIA_ROOT)