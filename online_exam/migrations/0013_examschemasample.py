# Generated by Django 3.2.4 on 2021-07-02 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_exam', '0012_samplequestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamSchemaSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wing', models.CharField(default='Army', max_length=150)),
                ('subject', models.CharField(max_length=150)),
                ('questions', models.CharField(default=4, max_length=150, verbose_name='Allotted Questions')),
                ('marks', models.CharField(default=5, max_length=150, verbose_name='Marks per question')),
                ('pass_percentage', models.IntegerField(default=40)),
            ],
        ),
    ]