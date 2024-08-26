from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


class Banners(models.Model):
    img = models.ImageField(upload_to="banners")
    alt_text = models.CharField(max_length=100)

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

    def __str__(self) -> str:
        return self.title
    

# Above subscription types features
class SubscriptionPlansFeatures(models.Model):
    subplan = models.ManyToManyField(SubscriptionPlans)
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title
    

# # The person to subscribe to a subscription Plan
class Subscriber(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile = models.CharField()
    address = models.TextField(max_length=100)
    img = models.ImageField(upload_to="subs")

    def __str__(self) -> str:
        return  self.user

    def image_tag(self):
        return mark_safe('<img src="%s" width ="80"/>' %(self.img.url))


# #The type of subscription done by user
class SubscriptionType(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    plan = models.ForeignKey(SubscriptionPlans, on_delete=models.CASCADE, null=True)
    price = models.IntegerField()
    

class Trainer(models.Model):
    full_name = models.CharField(max_length=50)
    mobile = models.IntegerField()
    address = models.TextField()
    is_active = models.BooleanField(default=False)
    details = models.TextField()
    img = models.ImageField(upload_to="trainers")

    def __str__(self) -> str:
        return self.full_name
    
    def image_tag(self):
        if self.img:
            return mark_safe('<img src="%s" width ="80"/>' %(self.img.url))