# Generated by Django 3.2.4 on 2021-07-01 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certexam', '0017_cadet_appeared_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadet',
            name='mobile',
            field=models.CharField(help_text='Enter 10 digit mobile number', max_length=12, verbose_name='Mobile Number'),
        ),
        migrations.AlterField(
            model_name='school',
            name='school',
            field=models.CharField(max_length=150, verbose_name='Institute'),
        ),
    ]