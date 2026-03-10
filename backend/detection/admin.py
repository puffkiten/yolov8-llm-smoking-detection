from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Camera, DetectionTask, SmokingRecord

# 把我们的三张核心业务表注册到 Django 自带的后台管理系统中
admin.site.register(Camera)
admin.site.register(DetectionTask)
admin.site.register(SmokingRecord)