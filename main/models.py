from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

class Banners(models.Model):
    img = models.ImageField(upload_to="banners")
    alt_text = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Banners'

    def __str__(self) -> str:
        return self.alt_text
    
    def image_tag(self):
        return mark_safe('<img src="%s" width ="80"/>' %(self.img.url))

class Service(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField(max_length=150)
    img = models.ImageField(upload_to="services")

    def __str__(self) -> str:
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width ="80"/>' %(self.img.url))

class Page(models.Model):
    title = models.TextField(max_length=100)
    detail = models.TextField(max_length=100)

    def __str__(self):
        return self.title
    

class Faq(models.Model):
    question = models.TextField(max_length=100)
    answer = models.TextField(max_length=100)

    def __str__(self):
        return self.question
    

class Enquiry(models.Model):
    full_name = models.CharField(max_length=100)
    query = models.TextField(max_length=100)
    email = models.CharField(max_length=20)
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    

class Gallery(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField(max_length=150)
    img = models.ImageField(upload_to="gallery")

    def __str__(self) -> str:
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width ="80"/>' %(self.img.url))
    
class GalleryImages(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE,null=True)
    alt_text = models.CharField(max_length=50)
    img = models.ImageField(upload_to="gallery_imgs")

    class Meta:
        verbose_name_plural = 'Gallery Images'

    def __str__(self) -> str:
        return self.alt_text
    
    def image_tag(self):
        return mark_safe('<img src="%s" width ="80"/>' %(self.img.url))


# basic standard ... types of subsciptions 
class  SubscriptionPlans(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    max_members = models.IntegerField(null=True)
    highlight_status = models.BooleanField(default=False,null=True)
    validity = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'Subscription Plans'
    
    def __str__(self) -> str:
        return self.title
    

# Above subscription types features
class SubscriptionPlansFeatures(models.Model):
    subplan = models.ManyToManyField(SubscriptionPlans)
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Subscription Plans Features'
    
    def __str__(self) -> str:
        return self.title
    

# The person to subscribe to a subscription Plan
class Subscriber(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile = models.CharField()
    address = models.TextField(max_length=100)
    img = models.ImageField(upload_to="subs")

    def __str__(self) -> str:
        return  str(self.user)  

    def image_tag(self):
        return mark_safe('<img src="%s" width ="80"/>' %(self.img.url))


# while doing the subscription
class SubscriptionType(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    plan = models.ForeignKey(SubscriptionPlans, on_delete=models.CASCADE, null=True)
    price = models.IntegerField()
    reg_date = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.user.username)
    

class Trainer(models.Model):
    full_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=50,null=True)
    mobile = models.IntegerField()
    address = models.TextField()
    is_active = models.BooleanField(default=False)
    details = models.TextField()
    img = models.ImageField(upload_to="trainers")
    social_links = models.JSONField(blank=True,null=True)
    month_salary = models.IntegerField(null=True)
    

    def __str__(self) -> str:
        return self.full_name
    
    def image_tag(self):
        if self.img:
            return mark_safe('<img src="%s" width ="80"/>' %(self.img.url))
        

class TrainerAcheivements(models.Model):
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE)
    title = models.CharField(max_length=100) 
    date_awarded = models.DateField()  
    description = models.TextField(max_length=300, blank=True) 
    badge_image = models.ImageField(upload_to='achievement_badges/', blank=True)

    def __str__(self) -> str:
        return self.title
    
    def image_tag(self):
        if self.badge_image:
            return mark_safe('<img src="%s" width ="80"/>' %(self.badge_image.url))


class TrainerSalary(models.Model):
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE)
    amount = models.IntegerField()
    deposit_date = models.DateTimeField()
    remarks = models.TextField(blank=True)

    def __str__(self) -> str:
        return str(self.amount)
    
#just giving notification to trainer by admin
class TrainerNotification(models.Model):
    notif_msg = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.notif_msg)
    
    def save(self, *args, **kwargs):
        super(TrainerNotification, self).save(*args, **kwargs)

        channel_layer = get_channel_layer()
        notif = self.notif_msg
        notif_id = self.pk  # Get the primary key (ID) after saving
        total = TrainerNotification.objects.filter(is_read=False).count()

        async_to_sync(channel_layer.group_send)(
            'noti_group_name',
            {
                'type': 'send_notification',
                'value': json.dumps({
                    'notif_id': notif_id, 
                    'notif': notif,
                    'total': total,
                    'action': 'add' 
                })
            }
        )

    def delete(self, *args, **kwargs):
        notif_id = self.pk
        super(TrainerNotification, self).delete(*args, **kwargs)
        
        channel_layer = get_channel_layer()
        total = TrainerNotification.objects.filter(is_read=False).count()

        async_to_sync(channel_layer.group_send)(
            'noti_group_name',
            {
                'type': 'send_notification',
                'value': json.dumps({
                    'notif_id': notif_id,
                    'total': total,
                    'action': 'delete'
                })
            }
        )


# # Trainer notifications
# class NotifTrainerStatus(models.Model):
#     notif = models.ForeignKey(TrainerNotification, on_delete=models.CASCADE)
#     trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
#     status = models.BooleanField(default=False)

#     class Meta:
#         verbose_name_plural = 'Trainer Notifications Status'

#     def __str__(self) -> str:
#         return str(self.notif)


    
# User Notifications and response via ajax
class Notify(models.Model):
    notify_detail = models.TextField()
    read_by_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    read_by_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) ->str:
        return self.notify_detail
    

# Mark as read notifications by user
class NotifUserStatus(models.Model):
    notif = models.ForeignKey(Notify, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Notifications Status'

# Assign a subscriber to the trainer
class AssignSubscriber(models.Model):
    subscriber = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.subscriber)
    

# Subscriber messages to trainer 
class TrainerMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE,null=True)
    message = models.TextField()

    class Meta:
        verbose_name_plural = 'Messages to Trainers'

    def __str__(self) -> str:
        return self.message
