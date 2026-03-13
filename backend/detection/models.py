from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    annotated_file = models.FileField(upload_to='results/tasks/', blank=True, null=True, verbose_name="带框结果文件")
    confidence_threshold = models.FloatField(default=0.5, verbose_name="置信度阈值")
    model_name = models.CharField(max_length=80, default="Aero-YOLO-v8s", verbose_name="检测模型")
    device_name = models.CharField(max_length=80, default="GPU", verbose_name="运行设备")
    status = models.CharField(max_length=20,
                              choices=(('pending', '等待中'), ('processing', '检测中'), ('completed', '已完成'), ('failed', '任务中断')),
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True, verbose_name="完成时间")
    file_size = models.BigIntegerField(default=0, verbose_name="文件大小字节")
    resolution_w = models.IntegerField(default=0, verbose_name="宽度")
    resolution_h = models.IntegerField(default=0, verbose_name="高度")
    process_time_ms = models.IntegerField(default=0, verbose_name="处理耗时毫秒")
    detections = models.JSONField(default=list, verbose_name="检测框")
    verify_status = models.CharField(
        max_length=20,
        choices=(
            ('pending', '待核实'),
            ('verified', '已核实'),
        ),
        default='verified',
        verbose_name="核实状态",
    )
    verify_result = models.CharField(
        max_length=20,
        choices=(
            ('pass', '核实通过'),
            ('violation', '标记违规'),
        ),
        blank=True,
        null=True,
        default=None,
        verbose_name="核实结果",
    )
    error_message = models.CharField(max_length=500, blank=True, null=True, verbose_name="错误原因")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建人")


class ShareLink(models.Model):
    token = models.CharField(max_length=80, unique=True, db_index=True, verbose_name="分享令牌")
    task = models.ForeignKey(DetectionTask, on_delete=models.CASCADE, related_name="share_links", verbose_name="关联任务")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建人")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    expires_at = models.DateTimeField(blank=True, null=True, verbose_name="过期时间")
    revoked = models.BooleanField(default=False, verbose_name="是否已撤销")

    def is_expired(self):
        return bool(self.expires_at and timezone.now() >= self.expires_at)


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
