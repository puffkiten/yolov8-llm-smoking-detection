"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
# backend/backend/urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView # 👈 引入官方原生视图
from detection.views import detect_image
from detection.views import upload_detection, tasks_list, task_detail, task_export, task_retry, task_share_create, share_report, task_verify, dashboard_trend
from detection.auth_views import (
    password_reset_request,
    password_reset_confirm,
    google_login,
    google_callback,
    register,
    me,
    users_list,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/detect/', detect_image),
    path('api/detection/upload', upload_detection),
    path('api/detection/tasks', tasks_list),
    path('api/detection/tasks/<int:task_id>', task_detail),
    path('api/detection/tasks/<int:task_id>/export', task_export),
    path('api/detection/tasks/<int:task_id>/retry', task_retry),
    path('api/detection/tasks/<int:task_id>/verify', task_verify),
    path('api/detection/tasks/<int:task_id>/share', task_share_create),
    path('api/share/report', share_report),
    path('api/dashboard/trend', dashboard_trend),
    # 👈 直接使用官方视图，把它绑定到 login 路由上
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    # 忘记密码
    path('api/auth/password-reset/request', password_reset_request, name='password_reset_request'),
    path('api/auth/password-reset/confirm', password_reset_confirm, name='password_reset_confirm'),
    # Google OAuth
    path('api/auth/google/login', google_login, name='google_login'),
    path('api/auth/google/callback', google_callback, name='google_callback'),
    # 注册与用户信息
    path('api/auth/register', register, name='register'),
    path('api/me', me, name='me'),
    path('api/users', users_list, name='users_list'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
