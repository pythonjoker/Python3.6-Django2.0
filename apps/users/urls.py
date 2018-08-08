# coding:utf-8
__author__ = 'Tone'
__date__ = '2018/8/6 '
from django.urls import path,re_path
from .views import UserInfoView,UplodImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView,MyCourseView,MyFavOrgView,MyFavCourseView,MyFavTeacherView,MyMessageView
app_name = 'users'

urlpatterns = [

    path('info/',UserInfoView.as_view(),name='user_info'),
    path('upload/image/',UplodImageView.as_view(),name='upload_image'),
    path('update/pwd/',UpdatePwdView.as_view(),name='update_pwd'),
    path('sendemail_code/',SendEmailCodeView.as_view(),name='sendemail_code'),
    path('update_email/',UpdateEmailView.as_view(),name='update_email'),
    path('my/course/',MyCourseView.as_view(),name='mycourse'),
    path('myfav/org/',MyFavOrgView.as_view(),name='myfav_org'),
    path('myfav/course/',MyFavCourseView.as_view(),name='myfav_course'),
    path('myfav/teacher/',MyFavTeacherView.as_view(),name='myfav_teacher'),
    path('my/message/',MyMessageView.as_view(),name='my_message'),
]