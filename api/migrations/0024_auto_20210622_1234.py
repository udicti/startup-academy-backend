# Generated by Django 3.0.5 on 2021-06-22 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20210622_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='password',
        ),
    ]
