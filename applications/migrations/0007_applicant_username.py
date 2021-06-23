# Generated by Django 3.0.5 on 2021-06-23 14:39

import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0006_remove_applicant_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='username',
            field=models.CharField(default=django.utils.timezone.now, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
            preserve_default=False,
        ),
    ]
