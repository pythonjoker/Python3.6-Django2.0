from django.db import models
from django.utils import timezone
from organization.models import CourseOrg,Teacher
from DjangoUeditor.models import UEditorField
# Create your models here.


# 课程表
class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj',u'初级'),
        ('zj', u'中级'),
        ('gj', u'高级')
    )
    name = models.CharField(max_length=50,verbose_name=u'课程名')
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True, blank=True,verbose_name=u'讲师')
    desc = models.CharField(max_length=200,verbose_name=u'课程描述')
    detail = UEditorField(width=600, height=300, imagePath="course/ueditor/image/",
                           filePath="course/ueditor/file/",verbose_name=u'课程详情',default='')
    tag = models.CharField(max_length=15,verbose_name=u'课程标签',default=u'')
    Notice = models.CharField(max_length=50,verbose_name=u'课程公告',default=u'欢迎学习本课程')
    teacher_tell = models.CharField(max_length=100,verbose_name=u'老师告诉你',default=u'你什么都能学到')
    you_need = models.CharField(max_length=100,verbose_name=u'课程须知',default=u'本课程适合零基础想入门的同学')
    course_org = models.ForeignKey(CourseOrg,on_delete=models.CASCADE, verbose_name=u"所属机构", null=True, blank=True)
    degree = models.CharField(choices=DEGREE_CHOICES,max_length=2)
    learn_times = models.IntegerField(default=0,verbose_name=u'学习时长')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    click_nums=models.IntegerField(default=0,verbose_name=u'点击数')
    is_banner = models.BooleanField(default=False,verbose_name=u'是否首页推荐')
    add_time = models.DateField(default=timezone.now,verbose_name=u'添加时间')
    image = models.ImageField(
        upload_to='course/%Y/%m',
        verbose_name=u'封面图',
        max_length=100
    )

    class Meta:
        verbose_name = u'课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 取章节数
    def get_zj_nums(self):
        return self.lesson_set.all().count()

    get_zj_nums.short_description = '章节数'

    # 取学习人数前五
    def get_students(self):
        return self.usercourse_set.all()[:5]


class BannerCourse(Course):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


# 章节表
class Lesson(models.Model):
    # 外键指明章节所对应的课程
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name=u'课程')
    name = models.CharField(max_length=50,verbose_name=u'章节名')
    add_time = models.DateField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》>> {1}'.format(self.course, self.name)

    def get_video(self):
        return self.video_set.all()



# 章节视频信息
class Video(models.Model):
    # 外键指明视频所对应的章节
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,verbose_name=u'章节')
    name = models.CharField(max_length=50, verbose_name=u'视频名')
    url = models.URLField(max_length=200,verbose_name=u'视频连接',default=u'')
    add_time = models.DateField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 课程资源
class CourseResource(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name=u'课程')
    name = models.CharField(max_length=50, verbose_name=u'资源名称')
    download = models.FileField(
        upload_to='course/resource/%Y/%m',
        verbose_name=u'资源文件',
        max_length=100)
    add_time = models.DateField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的 {1}'.format(self.course, self.name)