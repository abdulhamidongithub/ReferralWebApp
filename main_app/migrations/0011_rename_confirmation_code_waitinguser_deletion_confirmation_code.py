# Generated by Django 5.0.6 on 2024-06-15 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_faquestion_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='waitinguser',
            old_name='confirmation_code',
            new_name='deletion_confirmation_code',
        ),
    ]
