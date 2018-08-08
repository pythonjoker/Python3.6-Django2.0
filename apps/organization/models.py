from datetime import datetime

from django.db import models
# Create your models here.

# 城市
class CityDict(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'城市')
    desc = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 课程机构
class CourseOrg(models.Model):
    CATEGORG_CHOICES = (
        ('pxjg', u"培训机构"),
        ('gx', u"高校"),
        ('gr', u"个人")
    )
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    desc = models.CharField(max_length=200, verbose_name=u'机构描述')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name=u'所在城市')
    add_time = models.DateField(default=datetime.now, verbose_name=u'添加时间')
    image = models.ImageField(
        upload_to='org/%Y/%m',
        verbose_name=u'封面图',
        max_length=100
    )
    categorg = models.CharField(
        max_length=20,
        choices=CATEGORG_CHOICES,
        default='pxjg',
        verbose_name=u'机构类别'
    )

    class Meta:
        verbose_name = u'机构信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    # 取机构讲师数
    def get_teacher_nums(self):
        return self.teacher_set.all().count()


# 讲师
class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,on_delete=models.CASCADE,verbose_name=u'所属机构')
    name = models.CharField(max_length=50, verbose_name=u'讲师名称')
    work_years = models.IntegerField(default=0,verbose_name=u'工作年限')
    age = models.IntegerField(default=0,verbose_name=u'年龄')
    work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
    work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    image = models.ImageField(
        upload_to='teacher/%Y/%m',
        verbose_name=u'头像',
        max_length=100,
        default='teacher/default.png',
    )

    class Meta:
        verbose_name = u'讲师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_new_course(self):
        return self.course_set.order_by("-add_time")[:1]

    def get_course_nums(self):
        return len(self.course_set.all())