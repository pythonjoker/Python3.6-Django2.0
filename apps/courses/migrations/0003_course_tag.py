# Generated by Django 2.0.7 on 2018-08-05 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='', max_length=15, verbose_name='课程标签'),
        ),
    ]
