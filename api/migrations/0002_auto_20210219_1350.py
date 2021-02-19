# Generated by Django 3.0.5 on 2021-02-19 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='_id',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='_id',
        ),
        migrations.AddField(
            model_name='project',
            name='bussiness_idea',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='date_created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='is_profitable',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='members_in_udsm',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='problem_solved',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='to_whom',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='value_it_brings',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='admission_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='college',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='programme',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='study_period',
            field=models.IntegerField(blank=True, choices=[(3, 'Three'), (4, 'Four')], default=3),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='university',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='year_of_study',
            field=models.IntegerField(blank=True, default=2021),
        ),
        migrations.AlterField(
            model_name='project',
            name='owners',
            field=models.ManyToManyField(blank=True, related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(default='A title', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
