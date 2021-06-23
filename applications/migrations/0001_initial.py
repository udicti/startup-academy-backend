# Generated by Django 3.0.5 on 2021-06-22 21:06

import ckeditor.fields
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationWindow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('starts', models.DateField()),
                ('ends', models.DateField()),
                ('questions', models.ManyToManyField(related_name='application_window', to='applications.ApplicationQuestion', verbose_name='question')),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('university', models.CharField(max_length=255)),
                ('degree_program', models.CharField(max_length=255)),
                ('is_selected', models.BooleanField(default=False)),
                ('is_unselected', models.BooleanField(default=False)),
                ('application_window', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='applications.ApplicationWindow')),
            ],
            options={
                'verbose_name': 'Applicant',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', ckeditor.fields.RichTextField()),
                ('from_applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='applications.Applicant')),
                ('to_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='applications.ApplicationQuestion')),
            ],
        ),
    ]
