from .models import TrainerNotification

def notification_context(request):
    unread_count = TrainerNotification.objects.filter(is_read=False).count()
    return {
        'unread_count': unread_count,
    }