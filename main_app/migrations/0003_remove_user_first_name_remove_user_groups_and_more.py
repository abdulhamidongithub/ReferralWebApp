# Generated by Django 5.0.6 on 2024-05-31 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_rename_user_recommendation_referrer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
    ]
