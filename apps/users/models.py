from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class UserProfile(AbstractUser):
    # 性别选择规则
    GENDER_CHOICES = (
        ('male',u'男'),
        ('female',u'女')
    )
    # 昵称
    nick_name = models.CharField(max_length=50,verbose_name=u'昵称',default='')
    # 生日
    birthday = models.DateField(verbose_name=u'生日',null=True,blank=True)
    # 性别
    gender = models.CharField(
        max_length=7,
        verbose_name=u'性别',
        choices=GENDER_CHOICES,
        default='female'
    )
    # 地址
    address = models.CharField(max_length=100,verbose_name=u'地址',default='')
    # 手机号
    mobile = models.CharField(max_length=11,verbose_name=u'手机号',null=True,blank=True)
    # 头像 默认使用defaylt.png
    image = models.ImageField(
        upload_to='image/%Y/%m',
        default=u'image/default.png',
        max_length=100
    )

    # meta信息，即后台栏目名称
    class Meta:
        verbose_name='用户信息'
        verbose_name_plural = verbose_name

    # 重载str方法 username继承至AbstractUser
    def __str__(self):
        return self.username

    def unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id,has_read=False).count()

# 邮箱验证码
class EmailVerifyRecord(models.Model):
    # 自定义验证码类型
    SEND_CHOICES=(
        ('register',u'注册'),
        ('forget',u'找回密码'),
        ('update',u'修改邮箱')
    )
    code = models.CharField(max_length=20,verbose_name=u'验证码')
    email = models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type = models.CharField(choices=SEND_CHOICES,max_length=10)

    # now后的（）需要去掉 否者会根据编译时间，而不是实例化时间
    send_time = models.DateTimeField(default=timezone.now,verbose_name = u'发送时间')
    ex_time = models.DateTimeField(default=timezone.now,verbose_name = u'失效时间')
    has_use = models.BooleanField(default=False,verbose_name=u'是否使用')
    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural=verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)


# 轮播图
class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name=u'标题')
    image = models.ImageField(
        upload_to='banner/%Y/%m',
        verbose_name=u'轮播图',
        max_length=100
    )
    url = models.URLField(max_length=200,verbose_name=u'访问地址')
    # index越大越靠后
    index = models.IntegerField(default=100,verbose_name=u'顺序')
    add_time = models.DateField(default=timezone.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title




