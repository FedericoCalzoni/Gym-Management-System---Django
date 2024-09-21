from django.contrib import admin
from . import models

class BannerAdmin(admin.ModelAdmin):
    list_display = ('alt_text','image_tag')
admin.site.register(models.Banners,BannerAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title','image_tag')
admin.site.register(models.Service,ServiceAdmin)


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
    list_display = ('title','price','max_members','validity','highlight_status')
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
    list_display = ('user','plan','price','reg_date')
    
admin.site.register(models.SubscriptionType, SubscriptionTypeAdmin)


class TrainerAdmin(admin.ModelAdmin):
    list_editable = ('is_active',)
    list_display = ('full_name','mobile','month_salary','is_active','image_tag')
    
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


class TrainerAcheivementsAdmin(admin.ModelAdmin):
    list_display = ('trainer','title','date_awarded','description','image_tag')
    
admin.site.register(models.TrainerAcheivements, TrainerAcheivementsAdmin)


class TrainerSalaryAdmin(admin.ModelAdmin):
    list_display = ('trainer','amount','deposit_date','remarks')
    
admin.site.register(models.TrainerSalary, TrainerSalaryAdmin)


class TrainerNotificationAdmin(admin.ModelAdmin):
    list_display = ('notif_msg','is_read')

    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

admin.site.register(models.TrainerNotification, TrainerNotificationAdmin)


class TrainerMessageAdmin(admin.ModelAdmin):
    list_display = ('user','trainer','message')

admin.site.register(models.TrainerMessage, TrainerMessageAdmin)


class TrainerSubscriberReportAdmin(admin.ModelAdmin):
    list_display = ('get_sender', 'get_receiver', 'report_msg', 'created_at')

    def get_sender(self, obj):
        if obj.sender_trainer:
            return obj.sender_trainer
        else:
            return obj.sender_user
    get_sender.short_description = 'Sender'

    def get_receiver(self, obj):
        if obj.receiver_trainer:
            return obj.receiver_trainer
        else:
            return obj.receiver_user
    get_receiver.short_description = 'Receiver'

admin.site.register(models.TrainerSubscriberReport, TrainerSubscriberReportAdmin)


class MainLogoAdmin(admin.ModelAdmin):
    list_display = ('image_tag',)
    
admin.site.register(models.MainLogo, MainLogoAdmin)