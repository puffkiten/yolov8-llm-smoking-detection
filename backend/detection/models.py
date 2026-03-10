from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# 1. 摄像头管理表
class Camera(models.Model):
    name = models.CharField(max_length=100, verbose_name="摄像头名称")
    location = models.CharField(max_length=200, verbose_name="监控区域/位置")
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name="视频流URL或本地路径")
    threshold = models.FloatField(default=0.5, verbose_name="置信度阈值")
    status = models.IntegerField(choices=((0, '离线'), (1, '在线')), default=1, verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name


# 2. 检测任务表 (用于上传的视频或图片任务)
class DetectionTask(models.Model):
    task_name = models.CharField(max_length=100, verbose_name="任务名称")
    task_type = models.CharField(max_length=20, choices=(('image', '图片'), ('video', '视频')), verbose_name="任务类型")
    file_path = models.FileField(upload_to='uploads/tasks/', verbose_name="上传的文件")
    status = models.CharField(max_length=20,
                              choices=(('pending', '等待中'), ('processing', '检测中'), ('completed', '已完成')),
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建人")


# 3. 吸烟违规记录表 (仪表盘的数据来源，极其重要！)
class SmokingRecord(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="关联摄像头")
    task = models.ForeignKey(DetectionTask, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="关联任务")

    snapshot = models.ImageField(upload_to='snapshots/', verbose_name="抓拍截图")
    confidence = models.FloatField(verbose_name="YOLO置信度")
    llm_report = models.TextField(blank=True, null=True, verbose_name="大模型分析报告")

    is_confirmed = models.BooleanField(default=True, verbose_name="是否确认为吸烟(大模型复核结果)")
    detected_at = models.DateTimeField(auto_now_add=True, verbose_name="报警时间")

    def __str__(self):
        return f"违规记录 - {self.detected_at.strftime('%Y-%m-%d %H:%M:%S')}"