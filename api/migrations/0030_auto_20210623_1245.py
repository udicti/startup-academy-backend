# Generated by Django 3.0.5 on 2021-06-23 12:45

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0029_auto_20210622_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='commentreply',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mail',
            name='email_body',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='mail',
            name='to',
            field=models.ManyToManyField(blank=True, related_name='mails', to=settings.AUTH_USER_MODEL, verbose_name='recepient'),
        ),
        migrations.AlterField(
            model_name='project',
            name='bussiness_idea',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='problem_solved',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_cover',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_pic',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='to_whom',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='value_it_brings',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reviewreply',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.URLField(blank=True, null=True),
        ),
    ]
