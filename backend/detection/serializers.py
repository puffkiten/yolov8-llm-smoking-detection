from rest_framework import serializers

from .models import Camera, AIModel, ActiveModelConfig, LLMServiceConfig
import os
from django.conf import settings
from django.utils import timezone


def _camera_uses_uploaded_video(camera: Camera) -> bool:
    stream_url = str(getattr(camera, 'stream_url', '') or '').strip()
    if not stream_url:
        return False
    return stream_url.startswith('uploads/camera-files/') or os.path.splitext(stream_url)[1].lower() in {'.mp4', '.avi', '.mov', '.mkv', '.webm'}


def _camera_uploaded_video_exists(camera: Camera) -> bool:
    if not _camera_uses_uploaded_video(camera):
        return False
    candidate = str(camera.stream_url or '').lstrip('/')
    absolute = os.path.join(settings.MEDIA_ROOT, candidate)
    return os.path.exists(absolute)


def _camera_effective_online(camera: Camera) -> bool:
    if _camera_uploaded_video_exists(camera):
        return True
    if getattr(camera, 'is_online', False):
        last_active = getattr(camera, 'last_active', None)
        if not last_active:
            return True
        if timezone.is_naive(last_active):
            last_active = timezone.make_aware(last_active, timezone.get_current_timezone())
        return (timezone.now() - last_active).total_seconds() <= 300
    return False


class CameraSerializer(serializers.ModelSerializer):
    effective_is_online = serializers.SerializerMethodField()
    stream_kind = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = [
            "id",
            "name",
            "stream_url",
            "region",
            "confidence_threshold",
            "is_online",
            "effective_is_online",
            "stream_kind",
            "last_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_online", "effective_is_online", "stream_kind", "last_active", "created_at", "updated_at"]

    def get_effective_is_online(self, obj):
        return _camera_effective_online(obj)

    def get_stream_kind(self, obj):
        return 'file' if _camera_uses_uploaded_video(obj) else 'stream'


class AIModelSerializer(serializers.ModelSerializer):
    model_type_display = serializers.CharField(source='get_model_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AIModel
        fields = [
            'id',
            'name',
            'model_type',
            'model_type_display',
            'version',
            'status',
            'status_display',
            'accuracy',
            'deploy_node',
            'inference_threshold',
            'response_mode',
            'description',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'is_active', 'created_at', 'updated_at']


class AIModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = [
            'name',
            'model_type',
            'version',
            'status',
            'accuracy',
            'deploy_node',
            'inference_threshold',
            'response_mode',
            'description',
        ]

    def validate_name(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('模型名称不能为空')
        return value

    def validate_version(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('模型版本不能为空')
        return value

    def validate_accuracy(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError('精度必须在 0 到 1 之间')
        return value

    def validate_inference_threshold(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError('推理阈值必须在 0 到 1 之间')
        return value

    def validate(self, attrs):
        attrs['name'] = attrs.get('name', '').strip()
        attrs['version'] = attrs.get('version', '').strip()
        attrs['deploy_node'] = (attrs.get('deploy_node') or '').strip()
        attrs['description'] = (attrs.get('description') or '').strip()
        return attrs


class AIModelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = [
            'name',
            'model_type',
            'version',
            'status',
            'deploy_node',
            'inference_threshold',
            'response_mode',
            'accuracy',
            'description',
        ]

    def validate_name(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('模型名称不能为空')
        return value

    def validate_version(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('模型版本不能为空')
        return value

    def validate_accuracy(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError('精度必须在 0 到 1 之间')
        return value

    def validate_inference_threshold(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError('推理阈值必须在 0 到 1 之间')
        return value

    def validate(self, attrs):
        if 'name' in attrs:
            attrs['name'] = (attrs.get('name') or '').strip()
        if 'version' in attrs:
            attrs['version'] = (attrs.get('version') or '').strip()
        if 'deploy_node' in attrs:
            attrs['deploy_node'] = (attrs.get('deploy_node') or '').strip()
        if 'description' in attrs:
            attrs['description'] = (attrs.get('description') or '').strip()
        return attrs


class ActiveModelConfigSerializer(serializers.ModelSerializer):
    detection_model = AIModelSerializer(read_only=True)
    llm_model = AIModelSerializer(read_only=True)
    detection_model_id = serializers.PrimaryKeyRelatedField(
        queryset=AIModel.objects.filter(model_type=AIModel.MODEL_TYPE_DETECTION),
        source='detection_model',
        write_only=True,
        required=False,
        allow_null=True,
    )
    llm_model_id = serializers.PrimaryKeyRelatedField(
        queryset=AIModel.objects.filter(model_type=AIModel.MODEL_TYPE_LLM),
        source='llm_model',
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = ActiveModelConfig
        fields = [
            'id',
            'detection_model',
            'llm_model',
            'detection_model_id',
            'llm_model_id',
            'inference_threshold',
            'response_mode',
            'deploy_node',
            'updated_at',
        ]
        read_only_fields = ['id', 'updated_at']

    def validate_inference_threshold(self, value):
        if value < 0 or value > 1:
            raise serializers.ValidationError('推理阈值必须在 0 到 1 之间')
        return value

    def validate(self, attrs):
        detection_model = attrs.get('detection_model', getattr(self.instance, 'detection_model', None))
        llm_model = attrs.get('llm_model', getattr(self.instance, 'llm_model', None))
        if detection_model and detection_model.model_type != AIModel.MODEL_TYPE_DETECTION:
            raise serializers.ValidationError({'detection_model_id': '检测模型类型不正确'})
        if llm_model and llm_model.model_type != AIModel.MODEL_TYPE_LLM:
            raise serializers.ValidationError({'llm_model_id': '大语言模型类型不正确'})
        if 'deploy_node' in attrs:
            attrs['deploy_node'] = (attrs.get('deploy_node') or '').strip()
        return attrs


class LLMServiceListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    status_label = serializers.SerializerMethodField()
    model_identifier = serializers.SerializerMethodField()
    masked_api_key = serializers.SerializerMethodField()
    has_api_key = serializers.SerializerMethodField()

    class Meta:
        model = LLMServiceConfig
        fields = [
            'id',
            'service_key',
            'service_name',
            'model_identifier',
            'status',
            'status_label',
            'enabled',
            'is_connected',
            'base_url',
            'request_timeout',
            'masked_api_key',
            'has_api_key',
            'api_key_url',
            'sort_order',
            'updated_at',
        ]

    def get_status(self, obj):
        if obj.enabled:
            return 'enabled'
        if obj.api_key:
            return 'standby'
        return 'unconfigured'

    def get_status_label(self, obj):
        status = self.get_status(obj)
        return {
            'enabled': '已启用',
            'standby': '备用',
            'unconfigured': '未配置',
        }.get(status, '未配置')

    def get_model_identifier(self, obj):
        return obj.model_name or ''

    def get_masked_api_key(self, obj):
        key = (obj.api_key or '').strip()
        if not key:
            return ''
        if len(key) <= 8:
            return '*' * len(key)
        return f"{key[:3]}{'*' * (len(key) - 7)}{key[-4:]}"

    def get_has_api_key(self, obj):
        return bool((obj.api_key or '').strip())


class LLMServiceDetailSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    status_label = serializers.SerializerMethodField()
    masked_api_key = serializers.SerializerMethodField()
    has_api_key = serializers.SerializerMethodField()

    class Meta:
        model = LLMServiceConfig
        fields = [
            'id',
            'service_key',
            'service_name',
            'base_url',
            'model_name',
            'model_options',
            'api_key_url',
            'enabled',
            'is_connected',
            'request_timeout',
            'status',
            'status_label',
            'masked_api_key',
            'has_api_key',
            'last_tested_at',
            'updated_at',
        ]

    def get_status(self, obj):
        if obj.enabled:
            return 'enabled'
        if obj.api_key:
            return 'standby'
        return 'unconfigured'

    def get_status_label(self, obj):
        status = self.get_status(obj)
        return {
            'enabled': '已启用',
            'standby': '备用',
            'unconfigured': '未配置',
        }.get(status, '未配置')

    def get_masked_api_key(self, obj):
        key = (obj.api_key or '').strip()
        if not key:
            return ''
        if len(key) <= 8:
            return '*' * len(key)
        return f"{key[:3]}{'*' * (len(key) - 7)}{key[-4:]}"

    def get_has_api_key(self, obj):
        return bool((obj.api_key or '').strip())


class LLMServiceSaveSerializer(serializers.Serializer):
    service_key = serializers.CharField(max_length=32)
    model_name = serializers.CharField(max_length=120)
    api_key = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    enabled = serializers.BooleanField(required=False, default=False)
    request_timeout = serializers.IntegerField(required=False, min_value=1, max_value=300, default=30)

    def validate_service_key(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('服务商不能为空')
        if not LLMServiceConfig.objects.filter(service_key=value).exists():
            raise serializers.ValidationError('不支持的服务商')
        return value

    def validate_model_name(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('模型名称不能为空')
        return value

    def validate_api_key(self, value):
        return (value or '').strip()

    def validate(self, attrs):
        service = LLMServiceConfig.objects.get(service_key=attrs['service_key'])
        model_name = attrs['model_name']
        options = service.model_options or []
        if model_name not in options:
            raise serializers.ValidationError({'model_name': '所选模型不属于当前服务商'})
        final_api_key = (attrs.get('api_key') or '').strip() or (service.api_key or '').strip()
        if not final_api_key:
            raise serializers.ValidationError({'api_key': 'API Key 不能为空'})
        attrs['api_key'] = final_api_key
        return attrs


class LLMServiceSwitchSerializer(serializers.Serializer):
    service_key = serializers.CharField(max_length=32)

    def validate_service_key(self, value):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError('服务商不能为空')
        try:
            service = LLMServiceConfig.objects.get(service_key=value)
        except LLMServiceConfig.DoesNotExist as exc:
            raise serializers.ValidationError('不支持的服务商') from exc
        if not (service.api_key or '').strip():
            raise serializers.ValidationError('该服务尚未配置 API Key')
        if not (service.model_name or '').strip():
            raise serializers.ValidationError('该服务尚未配置模型名称')
        self.instance = service
        return value

