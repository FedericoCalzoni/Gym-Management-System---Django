from django import template
from main.models import SubscriptionPlans, SubscriptionType
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def check_purchased_package(user_id, plan_id=None):
    user = User.objects.get(id=user_id)
    
    if plan_id:
        # Check if the specific plan is purchased
        plan = SubscriptionPlans.objects.get(id=plan_id)
        purchased_package = SubscriptionType.objects.filter(user=user, plan=plan).exists()
        return purchased_package
    
    # Check if any plan is purchased
    purchased_any = SubscriptionType.objects.filter(user=user).exists()
    return purchased_any
