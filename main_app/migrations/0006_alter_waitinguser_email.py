# Generated by Django 5.0.6 on 2024-06-02 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitinguser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]