from .models import TrainerNotification,MainLogo
from django.utils.safestring import mark_safe

def notification_context(request):
    unread_count = TrainerNotification.objects.filter(is_read=False).count()
    return {
        'unread_count': unread_count,
    }

def logo(request):
    logo_image = MainLogo.objects.first() 

    if logo_image and logo_image.logo_image:
        data = {
            'logo': mark_safe('<img src="%s" width="35"/>' % (logo_image.logo_image.url))
        }
    else:
        data = {
            'logo': ''
        }

    return data
