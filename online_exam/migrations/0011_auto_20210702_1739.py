# Generated by Django 3.2.4 on 2021-07-02 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_exam', '0010_alter_examschema_pass_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentscore',
            name='wing',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='subject',
            field=models.CharField(blank=True, choices=[('Army', [('MR', 'MR'), ('Fd Craft/Battle Craft', 'Fd Craft/Battle Craft'), ('Mil History', 'Mil History'), ('Communication', 'Communication'), ('WE', 'WE')]), ('Navy', [('NO & GS', 'NO & GS'), ('Communication', 'Communication'), ('Navigation', 'Navigation'), ('Seamanship', 'Seamanship'), ('FF, DC & SS', 'FF, DC & SS'), ('Ship & BM', 'Ship & BM'), ('Swimming', 'Swimming')]), ('AF', [('General Service', 'General Service'), ('Air Campaign', 'Air Campaign'), ('Pr of Flight', 'Pr of Flight'), ('Airmanship', 'Airmanship'), ('Navigation', 'Navigation'), ('Airframe', 'Airframe'), ('AeroModelling', 'AeroModelling')])], max_length=150, null=True),
        ),
    ]
