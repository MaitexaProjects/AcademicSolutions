# Generated by Django 5.1.5 on 2025-02-02 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academiApp', '0015_remove_academiapp_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='academiapp',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
    ]
