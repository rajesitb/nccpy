# Generated by Django 3.2.4 on 2021-06-24 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certexam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_schools', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cadet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('sec_name', models.CharField(max_length=150)),
                ('dob', models.DateField(verbose_name='Date of Birth')),
                ('age', models.CharField(max_length=150)),
                ('number', models.IntegerField(verbose_name='NCC Number')),
                ('school', models.CharField(max_length=150)),
                ('email', models.EmailField(help_text='Enter Correct Email id of the student', max_length=254, verbose_name='Email Id')),
                ('mobile', models.IntegerField(help_text='Enter 10 digit mobile number', verbose_name='Mobile Number')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_cadet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
