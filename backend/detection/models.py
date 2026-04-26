from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AIModel(models.Model):
    MODEL_TYPE_DETECTION = 'detection'
    MODEL_TYPE_LLM = 'llm'
    MODEL_TYPE_STRATEGY = 'strategy'
    MODEL_TYPE_CHOICES = (
        (MODEL_TYPE_DETECTION, '目标检测'),
        (MODEL_TYPE_LLM, '大语言模型'),
        (MODEL_TYPE_STRATEGY, '策略模块'),
    )

    STATUS_ENABLED = 'enabled'
    STATUS_CONNECTED = 'connected'
    STATUS_STANDBY = 'standby'
    STATUS_CHOICES = (
        (STATUS_ENABLED, '已启用'),
        (STATUS_CONNECTED, '已连接'),
        (STATUS_STANDBY, '备用'),
    )

    name = models.CharField(max_length=120, unique=True, verbose_name='模型名称')
    model_type = models.CharField(max_length=20, choices=MODEL_TYPE_CHOICES, verbose_name='模型类型')
    version = models.CharField(max_length=80, verbose_name='版本')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_STANDBY, verbose_name='状态')
    accuracy = models.FloatField(default=0.0, verbose_name='精度')
    deploy_node = models.CharField(max_length=120, blank=True, default='', verbose_name='部署节点')
    inference_threshold = models.FloatField(default=0.75, verbose_name='推理阈值')
    response_mode = models.CharField(max_length=40, default='自动分析', verbose_name='响应模式')
    description = models.TextField(blank=True, default='', verbose_name='说明')
    is_active = models.BooleanField(default=False, verbose_name='是否当前激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['model_type', '-is_active', '-updated_at']
        verbose_name = 'AI 模型'
        verbose_name_plural = 'AI 模型'

    def __str__(self):
        return f'{self.name} ({self.version})'


class ActiveModelConfig(models.Model):
    detection_model = models.ForeignKey(
        AIModel,
        on_delete=models.PROTECT,
        related_name='active_for_detection',
        null=True,
        blank=True,
        verbose_name='当前检测模型',
    )
    llm_model = models.ForeignKey(
        AIModel,
        on_delete=models.PROTECT,
        related_name='active_for_llm',
        null=True,
        blank=True,
        verbose_name='当前大语言模型',
    )
    inference_threshold = models.FloatField(default=0.75, verbose_name='推理阈值')
    response_mode = models.CharField(max_length=40, default='自动分析', verbose_name='响应模式')
    deploy_node = models.CharField(max_length=120, blank=True, default='', verbose_name='部署节点')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最近更新时间')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='更新人')

    class Meta:
        verbose_name = '当前激活模型配置'
        verbose_name_plural = '当前激活模型配置'

    def __str__(self):
        return '当前激活模型配置'


class LLMServiceConfig(models.Model):
    SERVICE_QWEN = 'qwen'
    SERVICE_OPENAI = 'openai'
    SERVICE_DEEPSEEK = 'deepseek'
    SERVICE_ZHIPU = 'zhipu'
    SERVICE_CHOICES = (
        (SERVICE_QWEN, '通义千问'),
        (SERVICE_OPENAI, 'OpenAI GPT'),
        (SERVICE_DEEPSEEK, 'DeepSeek'),
        (SERVICE_ZHIPU, '智谱 AI'),
    )

    service_key = models.CharField(max_length=32, unique=True, choices=SERVICE_CHOICES, verbose_name='服务标识')
    service_name = models.CharField(max_length=64, verbose_name='服务名称')
    base_url = models.CharField(max_length=255, verbose_name='Base URL')
    api_key = models.CharField(max_length=255, blank=True, default='', verbose_name='API Key')
    model_name = models.CharField(max_length=120, blank=True, default='', verbose_name='模型名称')
    model_options = models.JSONField(default=list, verbose_name='模型选项')
    api_key_url = models.CharField(max_length=255, blank=True, default='', verbose_name='API Key 获取地址')
    enabled = models.BooleanField(default=False, verbose_name='是否启用')
    is_connected = models.BooleanField(default=False, verbose_name='连接状态')
    request_timeout = models.PositiveIntegerField(default=30, verbose_name='请求超时秒数')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='排序')
    last_tested_at = models.DateTimeField(blank=True, null=True, verbose_name='最近测试时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = '大模型服务配置'
        verbose_name_plural = '大模型服务配置'

    def __str__(self):
        return f'{self.service_name} ({self.model_name or "未配置"})'


# 1. 摄像头管理表（供“摄像头配置 / 实时监控”页面使用）
class Camera(models.Model):
    name = models.CharField(max_length=120, verbose_name="摄像头名称")
    # RTSP / HTTP / 本地设备号等
    stream_url = models.CharField(max_length=512, verbose_name="视频流地址")
    # 所属区域：例如“办公行政区”“生产仓库区”
    region = models.CharField(max_length=120, verbose_name="所属区域")
    # YOLO 置信度阈值
    confidence_threshold = models.FloatField(default=0.75, verbose_name="置信度阈值")
    # 在线状态：由后端探活或推理进程维护
    is_online = models.BooleanField(default=False, verbose_name="是否在线")
    # 最后一次心跳/推理时间
    last_active = models.DateTimeField(blank=True, null=True, verbose_name="最后活跃时间")
    # 创建 / 更新时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "摄像头"
        verbose_name_plural = "摄像头"

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
