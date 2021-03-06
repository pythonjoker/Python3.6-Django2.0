"""Djangtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import DjangoUeditor
import xadmin
from django.urls import path,include,re_path
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetPwdView,ModifyPwdView,LogoutView,IndexView
from django.views.static import serve

from .settings import MEDIA_ROOT

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    re_path(r'^ueditor/',include('DjangoUeditor.urls')),
    path('',IndexView.as_view(),name='index'),
    path('login/',LoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('captcha/',include('captcha.urls')),
    path('loguot/',LogoutView.as_view(),name='logout'),
    re_path(r'^media/(?P<path>.*)',serve,{"document_root": MEDIA_ROOT }),
    # re_path(r'^static/(?P<path>.*)',serve,{"document_root": STATIC_ROOT }),

    re_path('active/(?P<active_code>.*)/',ActiveUserView.as_view(),name='user_active'),
    re_path('reset/(?P<reset_code>.*)/',ResetPwdView.as_view(),name='reset'),
    path('forget/',ForgetPwdView.as_view(),name = 'forget'),
    path('modify_pwd/',ModifyPwdView.as_view(),name = 'modify_pwd'),

    path('cor/',include('courses.urls',namespace='cor')),
    path('org/',include('organization.urls',namespace='org')),
    path('user/',include('users.urls',namespace='user')),
]
# Django2.0中 在templates下创建404.html后 Django会自动寻找
# handler404 = 'users.views.page_not_found'
# handler500 = 'users.views.page_error'