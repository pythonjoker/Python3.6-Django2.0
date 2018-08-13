# coding:utf-8
__author__ = 'Tone'
__date__ = '2018/8/1 '

import xadmin
from .models import Course,Video,Lesson,CourseResource,BannerCourse
from organization.models import CourseOrg

class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name','desc','detail','degree','get_zj_nums','learn_times','students','click_nums','fav_nums']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name','desc','detail','degree','learn_times','students']
    ordering =['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline,CourseResourceInline]
    list_editable = ['degree', 'desc', ]
    style_fields = {'detail':'ueditor'}

    def queryset(self):
        qs = super(CourseAdmin,self).queryset()
        qs = qs.filter(is_banner = False)
        return qs

    def save_models(self):
        # 在保存课程时更新课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree','get_zj_nums', 'learn_times', 'students', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]
    list_editable = ['degree', 'desc', ]

    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner = True)
        return qs

class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    # __name代表使用外键中name字段
    list_filter = ['course__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

