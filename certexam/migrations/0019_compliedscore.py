# Generated by Django 3.2.4 on 2021-07-03 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certexam', '0018_auto_20210701_2312'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompliedScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_marks', models.CharField(blank=True, max_length=150, null=True)),
                ('marks_obtained', models.CharField(blank=True, max_length=150, null=True)),
                ('percentage', models.CharField(blank=True, max_length=150, null=True)),
                ('result', models.CharField(blank=True, max_length=150, null=True)),
                ('position', models.IntegerField(blank=True, null=True)),
                ('cadet', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cadet_compiled_result', to='certexam.cadet')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school_compiled_result', to='certexam.cadet')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_compiled_result', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]