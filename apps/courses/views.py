from django.shortcuts import render
from django.db.models import Q
from django.views.generic.base import View
from pure_pagination import Paginator,PageNotAnInteger
from .models import Course,CourseResource,Lesson,Video
from operation.models import UserFavorite,CourseComments,UserCourse
from django.http import HttpResponse

# Create your views here.

# 课程列表
class CourseListView(View):
    def get(self,request):
        all_courses= Course.objects.all()
        hot_courses= all_courses.order_by('-click_nums')[:3]
        sort = request.GET.get('sort', '')
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by("-students")
            elif sort == 'hot':
                all_courses = all_courses.order_by("-click_nums")
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 9, request=request)
        orgs = p.page(int(page))

        return render(request,'course-list.html',{
            'all_courses':orgs,
            'hot_courses':hot_courses,
            'sort':sort,
        })


# 课程详情
class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        has_fav_org = False
        has_fav_course = False
        tag = course.tag
        # 相关课程 若标签一致表示相关
        if tag:
            relate_courses = Course.objects.filter(tag = tag)[1:3]
        else:
            relate_courses = []

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request,'course-detail.html',{
            'course':course,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
            'relate_courses':relate_courses,
        })


# 章节信息
class CourseInfoView(View):
    def get(self,request,course_id):
        # 未登陆则跳转登陆页面
        if not request.user.is_authenticated:
            return render(request,'login.html',{})

        course = Course.objects.get(id=int(course_id))
        # 判断用户是否学过该门课程
        user = request.user
        try:
            has_course = UserCourse.objects.get(course=course,user=user)
        except:
            user_cor = UserCourse()
            user_cor.user = user
            user_cor.course = course
            user_cor.save()

        all_info = Lesson.objects.filter(course_id=int(course_id))
        all_resource = CourseResource.objects.filter(course_id=int(course_id))
        # 从用户课表中取出学过这门课的用户
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有学过用户的ID
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过ID取出所有学过的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 过滤掉当前课程
        course_ids = [ user_course.course_id for user_course in all_user_courses if user_course.course_id!=int(course_id)]
        # 按照点击数排序且只取前三
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[0:3]
        return render(request,'course-video.html',{
            'course':course,
            'all_resource':all_resource,
            'all_info':all_info,
            'relate_courses':relate_courses,
        })


# 课程评论
class CourseCommentView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id = int(course_id))
        all_resource = CourseResource.objects.filter(course_id=int(course_id))
        all_comment = CourseComments.objects.filter(course_id=int(course_id))
        all_comment = all_comment.order_by('-add_time')
        # 从用户课表中取出学过这门课的用户
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有学过用户的ID
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过ID取出所有学过的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 过滤掉当前课程
        course_ids = [user_course.course_id for user_course in all_user_courses if
                      user_course.course_id != int(course_id)]
        # 按照点击数排序且只取前三
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[0:3]
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_comment, 10, request=request)
        orgs = p.page(int(page))

        return render(request,'course-comment.html',{
            'course':course,
            'all_resource':all_resource,
            'all_comment':orgs,
            'relate_courses':relate_courses
        })


# 添加用户评论
class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if int(course_id)>0 and comments:
            course_comment = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


# 视频播放
class CoursePlayView(View):
    def get(self,request,video_id):
        # 未登陆则跳转登陆页面
        if not request.user.is_authenticated:
            return render(request,'login.html',{})

        video =Video.objects.get(id=int(video_id))
        course=video.lesson.course
        # 判断用户是否学过该门课程
        user = request.user
        try:
            has_course = UserCourse.objects.get(course=course,user=user)
        except:
            user_cor = UserCourse()
            user_cor.user = user
            user_cor.course = course
            user_cor.save()

        all_info = Lesson.objects.filter(course=course)
        all_resource = CourseResource.objects.filter(course=course)
        # 从用户课表中取出学过这门课的用户
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有学过用户的ID
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过ID取出所有学过的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 过滤掉当前课程
        course_ids = [ user_course.course_id for user_course in all_user_courses if user_course.course!=course]
        # 按照点击数排序且只取前三
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[0:3]
        return render(request,'course-play.html',{
            'course':course,
            'all_resource':all_resource,
            'all_info':all_info,
            'relate_courses':relate_courses,
            'video':video,
        })