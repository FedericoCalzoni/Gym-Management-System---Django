# Generated by Django 5.0.2 on 2024-08-11 17:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_gallery_galleryimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimages',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.gallery'),
        ),
    ]
