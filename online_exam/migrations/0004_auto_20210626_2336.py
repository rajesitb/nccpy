# Generated by Django 3.2.4 on 2021-06-26 18:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certexam', '0010_auto_20210626_1137'),
        ('online_exam', '0003_auto_20210626_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='subject',
            field=models.CharField(blank=True, choices=[('Army', [('MR', 'MR'), ('Fd Craft/Battle Craft', 'Fd Craft/Battle Craft'), ('Mil History', 'Mil History'), ('Communication', 'Communication'), ('WE', 'WE')]), ('Navy', [('NO & GS', 'NO & GS'), ('Communication', 'Communication'), ('Navigation', 'Navigation'), ('Seamanship', 'Seamanship'), ('FF, DC & SS', 'FF, DC & SS'), ('Ship & BM', 'Ship & BM'), ('Swimming', 'Swimming')]), ('Air', [('General Service', 'General Service'), ('Air Campaign', 'Air Campaign'), ('Pr of Flight', 'Pr of Flight'), ('Airmanship', 'Airmanship'), ('Navigation', 'Navigation'), ('Airframe', 'Airframe'), ('AeroModelling', 'AeroModelling')])], max_length=150, null=True),
        ),
        migrations.CreateModel(
            name='StudentScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=150)),
                ('score', models.IntegerField()),
                ('cadet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cadet_score', to='certexam.cadet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_score', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
