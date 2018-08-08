# Generated by Django 2.0.7 on 2018-08-05 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='Notice',
            field=models.CharField(default='欢迎学习本课程', max_length=50, verbose_name='课程公告'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(default='你什么都能学到', max_length=100, verbose_name='老师告诉你'),
        ),
        migrations.AddField(
            model_name='course',
            name='you_need',
            field=models.CharField(default='本课程适合零基础想入门的同学', max_length=100, verbose_name='课程须知'),
        ),
    ]