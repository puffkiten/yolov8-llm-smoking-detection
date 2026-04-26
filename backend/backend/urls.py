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
from detection.views import (
    detect_image,
    upload_detection,
    tasks_list,
    task_detail,
    task_export,
    task_retry,
    task_share_create,
    share_report,
    task_verify,
    dashboard_trend,
    cameras_stats,
    cameras_grouped,
    cameras_suggestions,
    CameraViewSet,
    camera_stream,
    AIModelViewSet,
    active_model_config,
    update_active_model_config,
    llm_service_overview,
    llm_service_list,
    llm_service_models,
    llm_current_config,
    llm_service_save,
    llm_service_test,
    llm_service_switch,
    camera_preview_stream,
)
from detection.auth_views import (
    password_reset_request,
    password_reset_confirm,
    google_login,
    google_callback,
    register,
    me,
    users_list,
    users_create,
    users_update,
    users_delete,
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'api/cameras', CameraViewSet, basename='camera')
router.register(r'api/ai-models', AIModelViewSet, basename='ai-model')


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
    path('api/cameras/stats/', cameras_stats),
    path('api/cameras/grouped/', cameras_grouped),
    path('api/cameras/suggestions/', cameras_suggestions),
    path('api/ai-models/active-config', active_model_config),
    path('api/ai-models/active-config/update', update_active_model_config),
    path('api/llm-services/overview', llm_service_overview),
    path('api/llm-services', llm_service_list),
    path('api/llm-services/current-config', llm_current_config),
    path('api/llm-services/save', llm_service_save),
    path('api/llm-services/test', llm_service_test),
    path('api/llm-services/switch', llm_service_switch),
    path('api/llm-services/<str:service_key>/models', llm_service_models),
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
    path('api/users/create', users_create, name='users_create'),
    path('api/users/<int:user_id>', users_update, name='users_update'),
    path('api/users/<int:user_id>/delete', users_delete, name='users_delete'),
    path('api/cameras/preview/stream/', camera_preview_stream, name='camera_preview_stream'),
    # 摄像头实时流
    path('api/cameras/<int:pk>/stream/', camera_stream, name='camera_stream'),
] + router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
