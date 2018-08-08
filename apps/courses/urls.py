# coding:utf-8
__author__ = 'Tone'
__date__ = '2018/8/4 '
from django.urls import path,re_path
from .views import CourseListView,CourseDetailView,CourseInfoView,CourseCommentView,AddCommentView,CoursePlayView

app_name = 'courses'

urlpatterns = [
    path('list',CourseListView.as_view(),name='cor_list'),
    re_path('detail/(?P<course_id>\d+)/',CourseDetailView.as_view(),name='cor_detail'),
    re_path('info/(?P<course_id>\d+)/',CourseInfoView.as_view(),name='cor_info'),
    re_path('comment/(?P<course_id>\d+)/',CourseCommentView.as_view(),name='cor_comment'),
    re_path('play/(?P<video_id>\d+)/',CoursePlayView.as_view(),name='cor_play'),
    path('add_comment',AddCommentView.as_view(),name='add_comment'),
]