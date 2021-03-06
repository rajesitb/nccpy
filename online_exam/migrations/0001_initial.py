# Generated by Django 3.2.4 on 2021-06-26 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=150)),
                ('question', models.CharField(max_length=300)),
                ('option_1', models.CharField(max_length=300)),
                ('option_2', models.CharField(max_length=300)),
                ('option_3', models.CharField(max_length=300)),
                ('option_4', models.CharField(max_length=300)),
                ('option_5', models.CharField(max_length=300)),
                ('option_6', models.CharField(max_length=300)),
                ('answer', models.IntegerField()),
            ],
        ),
    ]
