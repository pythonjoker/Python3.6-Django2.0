# Generated by Django 2.0.7 on 2018-08-08 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_is_bannes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='is_bannes',
            new_name='is_banner',
        ),
    ]
