# Generated by Django 5.0.6 on 2024-06-05 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_waitinguser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='waitinguser',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]