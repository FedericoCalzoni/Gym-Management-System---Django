# Generated by Django 5.0.2 on 2024-09-03 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_subscriptiontype_reg_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banners',
            options={'verbose_name_plural': 'Banners'},
        ),
        migrations.AlterModelOptions(
            name='galleryimages',
            options={'verbose_name_plural': 'Gallery Images'},
        ),
        migrations.AlterModelOptions(
            name='notifuserstatus',
            options={'verbose_name_plural': 'Notifications Status'},
        ),
        migrations.AlterModelOptions(
            name='subscriptionplans',
            options={'verbose_name_plural': 'Subscription Plans'},
        ),
        migrations.AlterModelOptions(
            name='subscriptionplansfeatures',
            options={'verbose_name_plural': 'Subscription Plans Features'},
        ),
        migrations.AddField(
            model_name='trainer',
            name='social_links',
            field=models.JSONField(blank=True, null=True),
        ),
    ]