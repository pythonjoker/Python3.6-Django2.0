# Generated by Django 2.0.7 on 2018-08-03 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180803_1829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailverifyrecord',
            old_name='exp_time',
            new_name='ex_time',
        ),
    ]
