from django.contrib import admin
from . import models

class BannerAdmin(admin.ModelAdmin):
    list_display = ('alt_text','image_tag')
admin.site.register(models.Banners,BannerAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title','image_tag')
admin.site.register(models.Service,ServiceAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(models.Page,PageAdmin)


class FaqAdmin(admin.ModelAdmin):
    list_display = ('question',)
admin.site.register(models.Faq,FaqAdmin)


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name','query','email','send_time')
admin.site.register(models.Enquiry,EnquiryAdmin)


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title','image_tag')
admin.site.register(models.Gallery,GalleryAdmin)


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('alt_text','image_tag')
admin.site.register(models.GalleryImages,GalleryImageAdmin)


class SubscriptionPlansAdmin(admin.ModelAdmin):
    list_editable = ('highlight_status','max_members')
    list_display = ('title','price','max_members','highlight_status')
admin.site.register(models.SubscriptionPlans, SubscriptionPlansAdmin)


class SubscriptionPlansFeaturessAdmin(admin.ModelAdmin):
    list_display = ('title','subplans')

    def subplans(self,obj):
        return " | ".join([sub.title for sub in obj.subplan.all()])
    
admin.site.register(models.SubscriptionPlansFeatures, SubscriptionPlansFeaturessAdmin)


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user','image_tag','mobile','address')
admin.site.register(models.Subscriber, SubscriberAdmin)


class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('user','plan','price')
    
admin.site.register(models.SubscriptionType, SubscriptionTypeAdmin)


class TrainerAdmin(admin.ModelAdmin):
    list_editable = ('is_active',)
    list_display = ('full_name','mobile','is_active','image_tag')
    
admin.site.register(models.Trainer, TrainerAdmin)


class NotifyAdmin(admin.ModelAdmin):
    list_display = ('notify_detail','read_by_user','read_by_trainer')
    
admin.site.register(models.Notify, NotifyAdmin)


class NotifUserStatusAdmin(admin.ModelAdmin):
    list_display = ('notif','user','status')
    
    class Meta:
        unique_together = ('notif', 'user')
admin.site.register(models.NotifUserStatus, NotifUserStatusAdmin)


class AssignSubscriberAdmin(admin.ModelAdmin):
    list_display = ('subscriber','trainer')
    
admin.site.register(models.AssignSubscriber, AssignSubscriberAdmin)



