# Generated by Django 5.0.2 on 2024-09-19 09:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_delete_notiftrainerstatus'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainerSubscriberReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_msg', models.TextField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('receiver_trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports_received_as_trainer', to='main.trainer')),
                ('receiver_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports_received_as_user', to=settings.AUTH_USER_MODEL)),
                ('sender_trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports_sent_as_trainer', to='main.trainer')),
                ('sender_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports_sent_as_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Trainer/User Reports',
            },
        ),
    ]
