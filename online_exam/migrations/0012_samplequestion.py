# Generated by Django 3.2.4 on 2021-07-02 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_exam', '0011_auto_20210702_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wing', models.CharField(choices=[('Army', 'Army'), ('Navy', 'Navy'), ('AF', 'AF')], default='Army', max_length=150)),
                ('subject', models.CharField(blank=True, choices=[('Army', [('MR', 'MR'), ('Fd Craft/Battle Craft', 'Fd Craft/Battle Craft'), ('Mil History', 'Mil History'), ('Communication', 'Communication'), ('WE', 'WE')]), ('Navy', [('NO & GS', 'NO & GS'), ('Communication', 'Communication'), ('Navigation', 'Navigation'), ('Seamanship', 'Seamanship'), ('FF, DC & SS', 'FF, DC & SS'), ('Ship & BM', 'Ship & BM'), ('Swimming', 'Swimming')]), ('AF', [('General Service', 'General Service'), ('Air Campaign', 'Air Campaign'), ('Pr of Flight', 'Pr of Flight'), ('Airmanship', 'Airmanship'), ('Navigation', 'Navigation'), ('Airframe', 'Airframe'), ('AeroModelling', 'AeroModelling')])], max_length=150, null=True)),
                ('question', models.CharField(blank=True, max_length=300, null=True)),
                ('option_1', models.CharField(default='Option number 1', max_length=300)),
                ('option_2', models.CharField(default='Option number 2', max_length=300)),
                ('option_3', models.CharField(default='Option number 3', max_length=300)),
                ('option_4', models.CharField(default='Option number 4', max_length=300)),
                ('option_5', models.CharField(default='Option number 5', max_length=300)),
                ('option_6', models.CharField(default='Option number 6', max_length=300)),
                ('answer', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
