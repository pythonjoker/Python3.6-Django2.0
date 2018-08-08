from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.http import HttpResponse
from .models import CourseOrg,CityDict,Teacher
from pure_pagination import Paginator,PageNotAnInteger
from .forms import AddUserAskForm
from operation.models import UserFavorite
from courses.models import Course
# Create your views here.

# 机构列表页
class OrgView(View):
    def get(self,request):
        all_org = CourseOrg.objects.all()
        all_city = CityDict.objects.all()
        hot_orgs = all_org.order_by('-click_nums')[:3]
        city_id =request.GET.get('city','')
        ct_id =request.GET.get('ct','')
        sort = request.GET.get('sort','')
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_org = all_org.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))
        if ct_id:
            all_org = all_org.filter(categorg=ct_id)
        if sort:
            if sort == 'students':
                all_org = all_org.order_by("-students")
            elif sort == 'courses':
                all_org = all_org.order_by("-course_nums")
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_org,5,request=request)
        orgs = p.page(page)
        org_nums = len(all_org)
        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_city':all_city,
            'org_nums':org_nums,
            'city_id':city_id,
            'ct_id':ct_id,
            'hot_orgs':hot_orgs,
            'sort':sort
        })

# 用户咨询
class AddUserAskView(View):
    def post(self,request):
        userask_form = AddUserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"输入有误请检查后再试"}',content_type='application/json')


# 机构首页
class OrgHomeView(View):
    def get(self,request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:2]
        has_fav = False
        course_org.click_nums += 1
        course_org.save()
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-homepage.html',{
            'current_page':current_page,
            'course_org':course_org,
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'has_fav': has_fav

        })

# 机构课程
class OrgCourseView(View):
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()


        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 10, request=request)
        orgs = p.page(int(page))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'current_page': current_page,
            'course_org': course_org,
            'all_courses': orgs,
            'has_fav': has_fav,
        })


# 机构介绍
class OrgDescView(View):
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'current_page': current_page,
            'course_org': course_org,
            'has_fav': has_fav
        })


# 机构课程
class OrgTeacherView(View):
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher, 5, request=request)
        orgs = p.page(int(page))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'current_page': current_page,
            'course_org': course_org,
            'all_teacher': orgs,
            'has_fav':has_fav
        })


# 用户收藏
class AddFavView(View):
    def post(self,request):
        id = request.POST.get('fav_id',0)
        type = request.POST.get('fav_type',0)
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        has_fav = False
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -= 1
                course.save()
            elif int(type) == 2:
                course_org = CourseOrg.objects.get(id=int(id))
                course_org.fav_nums -= 1
            elif int(type) == 3:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_nums -= 1
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            # 过滤掉未取到fav_id type的默认情况
            if int(type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()
                has_fav = True
                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:
                    course_org = CourseOrg.objects.get(id=int(id))
                    course_org.fav_nums += 1
                elif int(type) == 3:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

# 讲师列表页
class TeacherListView(View):
    def get(self,request):
        all_teachers = Teacher.objects.all()
        teacher_nums = len(all_teachers)
        sort = request.GET.get('sort', '')
        rank_teachers = all_teachers.order_by('-fav_nums')[:3]
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) | Q(points__icontains=search_keywords))
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 5, request=request)
        orgs = p.page(int(page))
        return render(request,'teachers-list.html',{
            'all_teachers':orgs,
            'teacher_nums':teacher_nums,
            'sort':sort,
            'rank_teachers':rank_teachers,
        })


# 讲师详情页
class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher_courses = Course.objects.filter(teacher=teacher)
        rank_teachers = Teacher.objects.filter(org=teacher.org).order_by('-fav_nums')[:3]
        has_fav_th = False
        has_fav_org = False
        teacher.click_nums +=1
        teacher.save()
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_th = True
            if UserFavorite.objects.filter(user=request.user,fav_id=teacher.org.id,fav_type=2):
                has_fav_org = True

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teacher_courses, 3, request=request)
        orgs = p.page(int(page))

        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'teacher_courses':orgs,
            'rank_teachers':rank_teachers,
            'has_fav_th':has_fav_th,
            'has_fav_org':has_fav_org,
        })