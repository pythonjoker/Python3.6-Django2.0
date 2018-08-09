import json
from django.db.models import Q
from django.shortcuts import render
from pure_pagination import Paginator,PageNotAnInteger
from django.contrib.auth import authenticate,login,logout
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile,EmailVerifyRecord,Banner
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm,UploadImageForm,UpdateUserInfoForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from django.utils import timezone
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from operation.models import UserCourse,UserFavorite,UserMessage
from courses.models import CourseOrg,Course
from organization.models import Teacher

# Create your views here.


# 使用邮箱和用户名均可登陆
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# 登陆
class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username','').strip().lower()
            pass_word = request.POST.get('password','')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, 'login.html', {'msg':'用户未激活'})
            else:
                return render(request,'login.html',{'msg':'账号或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 登出
class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

# 注册
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '').strip().lower()
            pass_word = request.POST.get('password', '')
            emailhsv = UserProfile.objects.filter(email=user_name)
            if emailhsv:
                return render(request, 'register.html', {'msg': '用户已存在请直接登录'})
            else:
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.password = make_password(pass_word)
                user_profile.is_active = False
                user_profile.save()
                user_message = UserMessage()
                user_message.user = user_profile.id
                user_message.message = "欢迎注册清客网"
                user_message.save()
                send_register_email(user_name,'register')
                return render(request,'login.html',{'msg':'注册成功 请在邮箱中激活后登录'})
        else:
            return render(request,'register.html',{'register_form':register_form})


# 激活
class ActiveUserView(View):
    def get(self,request,active_code):
        # 查询邮箱验证码记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code = active_code,has_use=False)
        if all_record:
            for record in all_record:
                # 验证码是否已过期
                if timezone.now() < record.ex_time:
                    email = record.email
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
                    record.has_use = True
                    record.save()
                    user.save()
                else:
                    return render(request, 'login.html', {'msg': '链接失效'})
            return render(request,'login.html',{'msg':'用户已成功激活 请登录'})
        else:
            return render(request,'login.html',{'msg':'链接失效'})


# 找回密码
class ForgetPwdView(View):
    def get(self,request):
        forgetpwd_form = ForgetPwdForm()
        return render(request,'forget-pwd.html',{'forgetpwd_form':forgetpwd_form})
    def post(self,request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email','')
            hav_user = UserProfile.objects.filter(email=email)
            if hav_user:
                send_register_email(email, 'forget')
                return render(request, 'login.html', {'msg': '重置密码邮件发送成功 请注意查收'})
            else:
                return render(request, 'forget-pwd.html', {'msg': '用户不存在', 'forgetpwd_form': forgetpwd_form})
        else:
            return render(request,'forget-pwd.html',{'forgetpwd_form':forgetpwd_form})


# 重置密码页面
class ResetPwdView(View):
    def get(self,request,reset_code):
        all_recode = EmailVerifyRecord.objects.filter(code=reset_code,has_use=False)
        if all_recode:
            for recode in all_recode:
                email = recode.email
                recode.has_use = True
                recode.save()
            return render(request,'reset-pwd.html',{'email':email,'reset_code':reset_code},)
        else:
            return render(request, 'login.html', {'msg': '链接失效或不存在'})


# 忘记密码修改密码
class ModifyPwdView(View):
    def post(self,request):
        modifypwd_form = ModifyPwdForm(request.POST)
        reset_code = request.POST.get('reset_code', '')
        if modifypwd_form.is_valid():
            pwd = request.POST.get('password','')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email','')
            all_email = EmailVerifyRecord.objects.filter(email=email,code=reset_code)
            if all_email:
                if pwd != pwd2:
                    return render(request,'reset-pwd.html',{'msg':'密码不一致','email':email,'reset_code':reset_code})
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd)
                user.save()
                return render(request,'login.html',{'msg':'密码修改成功请登录'})
            else:
                return render(request, 'login.html', {'msg': '非法访问'})
        else:
            email = request.POST.get("email", "")
            return render(request, 'reset-pwd.html', {'modifypwd_form':modifypwd_form, 'email': email,'reset_code':reset_code})


# 用户信息
class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'usercenter-info.html',{})
    def post(self,request):
        user_info_update =  UpdateUserInfoForm(request.POST,instance=request.user)
        if user_info_update.is_valid():
            user_info_update.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_update.errors), content_type='application/json')


# 修改头像
class UplodImageView(LoginRequiredMixin,View):
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


# 用户修改密码
class UpdatePwdView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd = request.POST.get('password','')
            pwd2 = request.POST.get('password2','')
            if pwd != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors),content_type='application/json')


# 发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixin,View):
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email,'update')
        return HttpResponse('{"status":"success"}', content_type='application/json')


# 修改邮箱
class UpdateEmailView(LoginRequiredMixin,View):
    def post(self,request):
        code = request.POST.get('code','')
        email = request.POST.get('email','')
        try:
            email_recode = EmailVerifyRecord.objects.get(code=code,email=email,has_use=False,send_type='update')
        except:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')
        if email_recode.ex_time > timezone.now():
            user = request.user
            user.email = email
            user.save()
            email_recode.has_use = True
            email_recode.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')


# 用户课程
class MyCourseView(LoginRequiredMixin,View):
    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(user_courses,4,request=request)
        message = p.page(page)

        return render(request,'usercenter-mycourse.html',{
            'user_courses':message,
        })


# 用户收藏机构
class MyFavOrgView(LoginRequiredMixin,View):
    def get(self,request):
        org_list=[]
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(org_list,4,request=request)
        message = p.page(page)

        return render(request,'usercenter-fav-org.html',{
            'all_fav_org':message,
        })


# 用户收藏课程
class MyFavCourseView(LoginRequiredMixin,View):
    def get(self,request):
        course_list=[]
        fav_courses = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(course_list,5,request=request)
        message = p.page(page)

        return render(request,'usercenter-fav-course.html',{
            'all_fav_course':message,
        })


# 用户收藏教师
class MyFavTeacherView(LoginRequiredMixin,View):
    def get(self,request):
        teacher_list=[]
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(teacher_list,4,request=request)
        message = p.page(page)

        return render(request,'usercenter-fav-teacher.html',{
            'all_fav_teacher':message,
        })


# 用户消息
class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        all_message = UserMessage.objects.filter(Q(user=request.user.id)|Q(user=0))
        all_unread_message = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message,5,request=request)
        message = p.page(page)
        return render(request,'usercenter-message.html',{
            'all_message':message,
        })


# 首页
class IndexView(View):
    def get(self,request):
        all_banners = Banner.objects.all().order_by('index')[:5]
        course_banners = Course.objects.filter(is_banner=True)[:3]
        courses = Course.objects.filter(is_banner=False)[:6]
        course_org = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'course_banners':course_banners,
            'courses':courses,
            'course_org':course_org,
        })


# 404
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response
