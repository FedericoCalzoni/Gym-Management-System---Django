# Generated by Django 5.0.2 on 2024-08-22 06:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_subscriptionplans_max_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlansDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_months', models.IntegerField()),
                ('total_discount', models.IntegerField()),
                ('subplan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.subscriptionplans')),
            ],
        ),
    ]
