# Generated by Django 3.2.4 on 2021-06-26 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_exam', '0002_auto_20210626_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='option_2',
            field=models.CharField(default='Option number 2', max_length=300),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_3',
            field=models.CharField(default='Option number 3', max_length=300),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_4',
            field=models.CharField(default='Option number 4', max_length=300),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_5',
            field=models.CharField(default='Option number 5', max_length=300),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_6',
            field=models.CharField(default='Option number 6', max_length=300),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(max_length=300, null=True),
        ),
    ]