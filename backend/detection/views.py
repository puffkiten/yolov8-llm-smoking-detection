from django.shortcuts import render

# Create your views here.
# 文件位置：backend/detection/views.py
import os
import threading
import secrets
import shutil
import subprocess
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db import close_old_connections
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from ultralytics import YOLO
from ai_core.llm_agent import analyze_smoking
from .models import DetectionTask, SmokingRecord, Camera, ShareLink, AIModel, ActiveModelConfig, LLMServiceConfig
from .serializers import (
    CameraSerializer,
    AIModelSerializer,
    ActiveModelConfigSerializer,
    LLMServiceListSerializer,
    LLMServiceDetailSerializer,
    LLMServiceSaveSerializer,
    LLMServiceSwitchSerializer,
)
import csv
import json
from io import StringIO
from urllib import error as urllib_error
from urllib import request as urllib_request

# 1. 启动时加载 YOLO 模型 (只加载一次，提高速度)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ai_core', 'best.pt')
model = YOLO(MODEL_PATH)


LLM_SERVICE_PRESETS = [
    {
        'service_key': LLMServiceConfig.SERVICE_QWEN,
        'service_name': '通义千问',
        'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        'model_options': ['qwen-turbo', 'qwen-plus', 'qwen-max', 'qwen-vl-max', 'qwen-vl-plus'],
        'model_name': 'qwen-turbo',
        'api_key_url': 'https://bailian.console.aliyun.com/',
        'sort_order': 10,
    },
    {
        'service_key': LLMServiceConfig.SERVICE_DEEPSEEK,
        'service_name': 'DeepSeek',
        'base_url': 'https://api.deepseek.com/v1',
        'model_options': ['deepseek-chat', 'deepseek-reasoner'],
        'model_name': 'deepseek-chat',
        'api_key_url': 'https://platform.deepseek.com/api_keys',
        'sort_order': 20,
    },
    {
        'service_key': LLMServiceConfig.SERVICE_OPENAI,
        'service_name': 'OpenAI GPT',
        'base_url': 'https://api.openai.com/v1',
        'model_options': ['gpt-4o-mini', 'gpt-4.1-mini', 'gpt-4o', 'gpt-4.1'],
        'model_name': 'gpt-4o-mini',
        'api_key_url': 'https://platform.openai.com/api-keys',
        'sort_order': 30,
    },
    {
        'service_key': LLMServiceConfig.SERVICE_ZHIPU,
        'service_name': '智谱 AI',
        'base_url': 'https://open.bigmodel.cn/api/paas/v4',
        'model_options': ['glm-4-flash', 'glm-4-air', 'glm-4-plus', 'glm-4v-plus'],
        'model_name': 'glm-4-flash',
        'api_key_url': 'https://open.bigmodel.cn/usercenter/apikeys',
        'sort_order': 40,
    },
]


def _mask_api_key(api_key: str) -> str:
    key = (api_key or '').strip()
    if not key:
        return ''
    if len(key) <= 8:
        return '*' * len(key)
    return f"{key[:3]}{'*' * (len(key) - 7)}{key[-4:]}"


def _ensure_llm_service_defaults():
    valid_keys = {preset['service_key'] for preset in LLM_SERVICE_PRESETS}
    LLMServiceConfig.objects.exclude(service_key__in=valid_keys).delete()
    for preset in LLM_SERVICE_PRESETS:
        defaults = {
            'service_name': preset['service_name'],
            'base_url': preset['base_url'],
            'model_options': preset['model_options'],
            'model_name': preset['model_name'],
            'api_key_url': preset['api_key_url'],
            'sort_order': preset['sort_order'],
        }
        service, created = LLMServiceConfig.objects.get_or_create(
            service_key=preset['service_key'],
            defaults=defaults,
        )
        changed = False
        for field, value in defaults.items():
            current = getattr(service, field)
            if field == 'model_name' and (service.model_name or '').strip():
                continue
            if current != value:
                setattr(service, field, value)
                changed = True
        if created:
            changed = True
        if changed:
            service.save()


def _get_enabled_llm_service():
    _ensure_llm_service_defaults()
    return LLMServiceConfig.objects.filter(enabled=True).order_by('sort_order', 'id').first()


def _sync_active_llm_model(service: LLMServiceConfig, user=None):
    if not service:
        return
    config = ActiveModelConfig.objects.order_by('id').first()
    if not config:
        config = ActiveModelConfig.objects.create()
    ai_model, _ = AIModel.objects.get_or_create(
        name=service.service_name,
        model_type=AIModel.MODEL_TYPE_LLM,
        defaults={
            'version': service.model_name or service.service_key,
            'status': AIModel.STATUS_ENABLED if service.enabled else AIModel.STATUS_STANDBY,
            'accuracy': 0.0,
            'deploy_node': service.base_url,
            'response_mode': '自动分析',
            'description': f'{service.service_name} 大模型服务',
            'is_active': service.enabled,
        },
    )
    ai_model.version = service.model_name or ai_model.version
    ai_model.deploy_node = service.base_url
    ai_model.status = AIModel.STATUS_ENABLED if service.enabled else AIModel.STATUS_STANDBY
    ai_model.is_active = bool(service.enabled)
    ai_model.save()
    if service.enabled:
        AIModel.objects.filter(model_type=AIModel.MODEL_TYPE_LLM).exclude(id=ai_model.id).update(is_active=False)
        config.llm_model = ai_model
        if user is not None:
            config.updated_by = user
        config.save(update_fields=['llm_model', 'updated_by', 'updated_at'])


def _get_model_category(model_name: str) -> str:
    value = (model_name or '').lower()
    multimodal_tokens = ('4o', 'vl', 'vision', '4v')
    return 'multimodal' if any(token in value for token in multimodal_tokens) else 'text'


def _test_llm_service_connection(service: LLMServiceConfig, api_key: str | None = None, model_name: str | None = None):
    final_key = (api_key if api_key is not None else service.api_key or '').strip()
    final_model = (model_name if model_name is not None else service.model_name or '').strip()
    if not final_key:
        return False, 'API Key 不能为空'
    if not final_model:
        return False, '模型名称不能为空'

    category = _get_model_category(final_model)
    content = [
        {'type': 'text', 'text': 'ping'}
    ] if category == 'multimodal' else 'ping'

    payload = json.dumps({
        'model': final_model,
        'messages': [{'role': 'user', 'content': content}],
        'max_tokens': 8,
    }).encode('utf-8')
    req = urllib_request.Request(
        url=f"{service.base_url.rstrip('/')}/chat/completions",
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {final_key}',
        },
        method='POST',
    )
    try:
        with urllib_request.urlopen(req, timeout=service.request_timeout or 30) as resp:
            status = getattr(resp, 'status', 200)
            if 200 <= status < 300:
                return True, f'{service.service_name} 连接测试通过'
            return False, f'{service.service_name} 连接测试失败，状态码 {status}'
    except urllib_error.HTTPError as exc:
        try:
            detail = exc.read().decode('utf-8', errors='ignore')[:200]
        except Exception:
            detail = ''
        return False, f'连接测试失败：HTTP {exc.code}{(" - " + detail) if detail else ""}'
    except Exception as exc:
        return False, f'连接测试失败：{str(exc)}'


def _build_llm_overview_payload():
    _ensure_llm_service_defaults()
    services = LLMServiceConfig.objects.all().order_by('sort_order', 'id')
    enabled_service = services.filter(enabled=True).first()
    current = enabled_service or services.first()
    connected = bool(current and current.is_connected)
    current_serializer = LLMServiceDetailSerializer(current) if current else None
    return {
        'detection_model': 'YOLOv8',
        'current_llm_name': current.service_name if current and current.enabled else '未启用',
        'connection_status': 'connected' if connected else 'disconnected',
        'connection_status_label': '已连接' if connected else '未连接',
        'services': LLMServiceListSerializer(services, many=True).data,
        'current_config': current_serializer.data if current_serializer else None,
        'current_provider': current.service_name if current else '',
        'current_model_name': current.model_name if current else '',
        'current_api_key_masked': _mask_api_key(current.api_key if current else ''),
        'current_base_url': current.base_url if current else '',
        'current_timeout': current.request_timeout if current else 30,
    }

def _normalize_verify_status(v):
    v = (v or '').strip()
    return 'pending' if v == 'pending' else 'verified'


@api_view(['POST'])
def detect_image(request):
    """前端上传图片的 API 接口"""
    # 1. 接收前端传来的图片文件
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({"error": "没有收到名为 'image' 的图片"}, status=400)

    # 2. 临时保存这张图片供 AI 分析
    temp_path = os.path.join(settings.BASE_DIR, 'temp_upload.jpg')
    with open(temp_path, 'wb+') as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    # 3. 呼叫 YOLO 进行毫秒级视觉检测！
    results = model.predict(source=temp_path, conf=0.5)

    has_smoking = False
    yolo_msg = "画面安全，未检测到吸烟行为。"

    # 解析 YOLO 的框
    for box in results[0].boxes:
        if int(box.cls[0]) == 0:  # 0 是我们训练的 cigarette 类别
            has_smoking = True
            yolo_msg = f"⚠️ YOLO 发现疑似香烟！(置信度: {float(box.conf[0]):.2f})"
            break  # 只要发现一个就算违规

    # 4. 复合判断：如果 YOLO 报警了，立刻呼叫大模型做最终定夺！
    llm_report = "YOLO 未发现异常，AI大脑无需介入。"
    if has_smoking:
        llm_report = analyze_smoking(temp_path)

    # 5. 把完整的鉴定报告打包发还给前端
    return Response({
        "status": "success",
        "has_smoking": has_smoking,
        "yolo_result": yolo_msg,
        "llm_report": llm_report
    })

def _clamp_conf(v):
    try:
        v = float(v)
    except Exception:
        v = 0.5
    return max(0.0, min(1.0, v))

def _fs():
    root = settings.MEDIA_ROOT
    os.makedirs(root, exist_ok=True)
    return FileSystemStorage(location=root)

def _predict_one(path, confidence=0.5):
    results = model.predict(source=path, conf=confidence)
    has_smoking = False
    boxes = []
    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        if cls == 0:
            has_smoking = True
        xyxy = box.xyxy[0].tolist()
        boxes.append({"cls": cls, "conf": conf, "xyxy": xyxy})
    shape = getattr(results[0], 'orig_shape', None)
    if shape and isinstance(shape, (list, tuple)) and len(shape) >= 2:
        h, w = int(shape[0] or 0), int(shape[1] or 0)
    else:
        orig_img = getattr(results[0], 'orig_img', None)
        if orig_img is not None and hasattr(orig_img, 'shape') and len(orig_img.shape) >= 2:
            h, w = int(orig_img.shape[0] or 0), int(orig_img.shape[1] or 0)
        else:
            h, w = 0, 0
    return has_smoking, boxes, (w, h)

def _ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def _results_fs():
    root = settings.MEDIA_ROOT
    _ensure_dir(root)
    return FileSystemStorage(location=root)

def _build_annotated_relpath(original_name: str) -> str:
    base = os.path.basename(original_name or "")
    stem, ext = os.path.splitext(base)
    ext = ext if ext else ".mp4"
    return os.path.join("results", "tasks", f"{stem}_annotated{ext}")

def _try_open_h264_writer(out_path: str, fps: float, w: int, h: int):
    import cv2
    for fourcc in ("avc1", "H264"):
        vw = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
        if vw.isOpened():
            return vw, fourcc
        vw.release()
    return None, ""

def _ffmpeg_available() -> bool:
    return bool(shutil.which("ffmpeg"))

def _ffmpeg_transcode_h264(in_path: str, out_path: str):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", in_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-an",
        out_path,
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        err = (p.stderr or b"").decode("utf-8", errors="ignore")[-2000:]
        raise RuntimeError(f"ffmpeg 转码失败: {err}")

def _process_video_task(dt: DetectionTask, input_path: str, confidence: float):
    import cv2
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError("无法打开视频文件")
    try:
        fps = cap.get(cv2.CAP_PROP_FPS) or 0
        if not fps or fps != fps:
            fps = 25.0
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        if not w or not h:
            raise RuntimeError("无法获取视频分辨率")

        fs = _results_fs()
        rel_out = _build_annotated_relpath(dt.file_path.name)
        abs_out = fs.path(rel_out)
        _ensure_dir(os.path.dirname(abs_out))

        writer, codec = _try_open_h264_writer(abs_out, fps, w, h)
        tmp_path = ""
        if writer is None:
            tmp_path = abs_out + ".tmp.mp4"
            writer = cv2.VideoWriter(tmp_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
            if not writer.isOpened():
                raise RuntimeError("无法初始化视频编码器")

        max_conf = 0.0
        frame_idx = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame_idx += 1
            results = model.predict(source=frame, conf=confidence, verbose=False)
            r0 = results[0]
            boxes = getattr(r0, "boxes", None)
            if boxes is not None and len(boxes) > 0:
                for b in boxes:
                    try:
                        if int(b.cls[0]) == 0:
                            max_conf = max(max_conf, float(b.conf[0]))
                    except Exception:
                        pass
            annotated = r0.plot()
            if annotated is None:
                annotated = frame
            writer.write(annotated)

        writer.release()
        cap.release()

        final_abs = abs_out
        if tmp_path:
            if not _ffmpeg_available():
                raise RuntimeError("当前环境无法直接输出 H.264（avc1），且未安装 ffmpeg，无法生成可播放的 MP4")
            _ffmpeg_transcode_h264(tmp_path, abs_out)
            try:
                os.remove(tmp_path)
            except Exception:
                pass

        dt.annotated_file = rel_out
        dt.file_size = os.path.getsize(final_abs) if os.path.exists(final_abs) else 0
        dt.resolution_w = w
        dt.resolution_h = h
        dt.detections = [{"label": "violation", "cls": 0, "conf": max_conf, "x": 0, "y": 0, "w": 0, "h": 0}] if max_conf > 0.0 else []
        dt.error_message = ''
        return (max_conf > 0.0), max_conf
    finally:
        try:
            cap.release()
        except Exception:
            pass

def _process_detection_task(task_id: int, confidence: float):
    close_old_connections()
    try:
        dt = DetectionTask.objects.get(id=task_id)
    except DetectionTask.DoesNotExist:
        return
    try:
        import time
        path = dt.file_path.path if hasattr(dt.file_path, 'path') else None
        if not path or not os.path.exists(path):
            raise FileNotFoundError("上传文件不存在或无法访问")

        t0 = time.time()
        has_smoking = False
        llm_report = ''
        boxes = []
        w = 0
        h = 0
        dets = []
        max_conf = 0.0
        if dt.task_type == 'video':
            has_smoking, max_conf = _process_video_task(dt, path, confidence)
            dt.verify_status = 'pending' if has_smoking else 'verified'
            dt.verify_result = None if has_smoking else 'pass'
        else:
            has_smoking, boxes, (w, h) = _predict_one(path, confidence)
            llm_report = analyze_smoking(path) if has_smoking else ''
            names = getattr(model, "names", {}) or {}
            if w and h:
                for b in boxes:
                    x1, y1, x2, y2 = b.get("xyxy", [0, 0, 0, 0])
                    cls = b.get("cls", -1)
                    confv = b.get("conf", 0.0)
                    label = names.get(cls, str(cls)) if isinstance(names, dict) else str(cls)
                    dets.append({
                        "label": label,
                        "cls": cls,
                        "conf": confv,
                        "x": max(0.0, min(100.0, (x1 / w) * 100.0)),
                        "y": max(0.0, min(100.0, (y1 / h) * 100.0)),
                        "w": max(0.0, min(100.0, ((x2 - x1) / w) * 100.0)),
                        "h": max(0.0, min(100.0, ((y2 - y1) / h) * 100.0)),
                    })
            dt.file_size = os.path.getsize(path)
            dt.resolution_w = w
            dt.resolution_h = h
            dt.detections = dets
            dt.verify_status = 'pending' if has_smoking else 'verified'
            dt.verify_result = None if has_smoking else 'pass'
        dt.process_time_ms = int((time.time() - t0) * 1000)
        dt.finished_at = timezone.now()
        dt.status = 'completed'
        dt.save()

        if has_smoking and dt.task_type == 'image':
            SmokingRecord.objects.create(
                camera=None,
                task=dt,
                snapshot=dt.file_path.name,
                confidence=max([b['conf'] for b in boxes if b['cls'] == 0] or [max_conf or confidence]),
                llm_report=llm_report,
                is_confirmed=True,
            )
    except Exception as exc:
        dt.status = 'failed'
        dt.error_message = f"{exc.__class__.__name__}: {str(exc)}"
        dt.finished_at = timezone.now()
        dt.verify_status = 'verified'
        dt.verify_result = None
        dt.save(update_fields=['status', 'error_message', 'finished_at', 'verify_status', 'verify_result'])
    finally:
        close_old_connections()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_detection(request):
    """
    提交检测任务：
    - 视频：单文件，创建 1 个 video 任务
    - 图片：支持单张或多张，逐张创建 image 任务
    - 字段：taskName, confidence, file (video) 或 files[] (images)
    """
    task_name = (request.data.get('taskName') or '').strip()
    confidence = _clamp_conf(request.data.get('confidence'))
    if not task_name:
        return Response({"detail": "任务名称不能为空"}, status=400)

    fs = _fs()
    created_tasks = []

    if 'file' in request.FILES:
        f = request.FILES['file']
        filename = fs.save(os.path.join('uploads', 'tasks', f.name), f)
        dt = DetectionTask.objects.create(
            task_name=task_name,
            task_type='video',
            file_path=filename,
            confidence_threshold=confidence,
            model_name='Aero-YOLO-v8s',
            device_name='GPU',
            status='processing',
            created_by=request.user,
        )
        created_tasks.append(dt)
    else:
        files = request.FILES.getlist('files')
        if not files:
            return Response({"detail": "请上传视频或图片文件"}, status=400)
        for index, f in enumerate(files, start=1):
            filename = fs.save(os.path.join('uploads', 'tasks', f.name), f)
            current_name = task_name if len(files) == 1 else f"{task_name}_{index}"
            dt = DetectionTask.objects.create(
                task_name=current_name,
                task_type='image',
                file_path=filename,
                confidence_threshold=confidence,
                model_name='Aero-YOLO-v8s',
                device_name='GPU',
                status='processing',
                created_by=request.user,
            )
            created_tasks.append(dt)

    for task in created_tasks:
        th = threading.Thread(target=_process_detection_task, args=(task.id, confidence), daemon=True)
        th.start()

    return Response({
        "code": 200,
        "id": created_tasks[0].id if created_tasks else None,
        "ids": [task.id for task in created_tasks],
        "created_count": len(created_tasks),
        "status": created_tasks[0].status if created_tasks else 'processing',
    }, status=202)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tasks_list(request):
    """
    任务列表（简版）
    """
    items = []
    qs = DetectionTask.objects.all() if request.user.is_staff else DetectionTask.objects.filter(created_by=request.user)
    for t in qs.order_by('-created_at'):
        created_local = timezone.localtime(t.created_at)
        finished_local = timezone.localtime(t.finished_at) if t.finished_at else None
        dets = t.detections or []
        det_count = len(dets) if isinstance(dets, list) else 0
        viol_count = 0
        if isinstance(dets, list):
            for d in dets:
                if isinstance(d, dict) and int(d.get("cls", -1)) == 0:
                    viol_count += 1
        items.append({
            "id": t.id,
            "name": t.task_name,
            "type": t.task_type,
            "status": t.status,
            "confidence": t.confidence_threshold,
            "verify_status": _normalize_verify_status(getattr(t, "verify_status", "verified")),
            "verify_result": getattr(t, "verify_result", None),
            "error_message": t.error_message or "",
            "detections_count": det_count,
            "violation_count": viol_count,
            "process_time_ms": t.process_time_ms or 0,
            "created_at": created_local.strftime('%Y-%m-%d %H:%M:%S'),
            "created_at_iso": created_local.isoformat(),
            "finished_at": finished_local.strftime('%Y-%m-%d %H:%M:%S') if finished_local else "",
            "finished_at_iso": finished_local.isoformat() if finished_local else "",
        })
    return Response({"results": items})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_detail(request, task_id: int):
    try:
        qs = DetectionTask.objects.all() if request.user.is_staff else DetectionTask.objects.filter(created_by=request.user)
        t = qs.get(id=task_id)
    except DetectionTask.DoesNotExist:
        return Response({"detail": "任务不存在"}, status=404)
    recs = SmokingRecord.objects.filter(task=t).order_by('-detected_at')
    records = []
    for r in recs:
        records.append({
            "id": r.id,
            "confidence": r.confidence,
            "snapshot": request.build_absolute_uri(r.snapshot.url) if hasattr(r.snapshot, 'url') else str(r.snapshot),
            "llm_report": r.llm_report or "",
            "detected_at": r.detected_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
    data = {
        "id": t.id,
        "name": t.task_name,
        "type": t.task_type,
        "status": t.status,
        "verify_status": _normalize_verify_status(getattr(t, "verify_status", "verified")),
        "verify_result": getattr(t, "verify_result", None),
        "created_at": timezone.localtime(t.created_at).strftime('%Y-%m-%d %H:%M:%S'),
        "created_at_iso": timezone.localtime(t.created_at).isoformat(),
        "finished_at": timezone.localtime(t.finished_at).strftime('%Y-%m-%d %H:%M:%S') if t.finished_at else "",
        "finished_at_iso": timezone.localtime(t.finished_at).isoformat() if t.finished_at else "",
        "file_size": t.file_size,
        "resolution": {"w": t.resolution_w, "h": t.resolution_h},
        "process_time_ms": t.process_time_ms,
        "original_url": request.build_absolute_uri(t.file_path.url) if hasattr(t.file_path, 'url') else str(t.file_path),
        "result_url": (
            request.build_absolute_uri(t.annotated_file.url)
            if (t.task_type == 'video' and getattr(t, 'annotated_file', None) and getattr(t.annotated_file, 'url', None))
            else (request.build_absolute_uri(t.file_path.url) if hasattr(t.file_path, 'url') else str(t.file_path))
        ),
        "source_url": request.build_absolute_uri(t.file_path.url) if hasattr(t.file_path, 'url') else str(t.file_path),
        "confidence": t.confidence_threshold,
        "model": t.model_name,
        "device": t.device_name,
        "error_message": t.error_message or "",
        "detections": t.detections or [],
        "records": records,
    }
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_export(request, task_id: int):
    try:
        qs = DetectionTask.objects.all() if request.user.is_staff else DetectionTask.objects.filter(created_by=request.user)
        t = qs.get(id=task_id)
    except DetectionTask.DoesNotExist:
        return Response({"detail": "任务不存在"}, status=404)
    recs = SmokingRecord.objects.filter(task=t).order_by('detected_at')
    sio = StringIO()
    writer = csv.writer(sio)
    writer.writerow(['record_id', 'detected_at', 'confidence', 'snapshot'])
    for r in recs:
        writer.writerow([r.id, r.detected_at.isoformat(), r.confidence, str(r.snapshot)])
    content = sio.getvalue()
    headers = {'Content-Type': 'text/csv', 'Content-Disposition': f'attachment; filename="task_{t.id}_export.csv"'}
    return Response(content, headers=headers)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_retry(request, task_id: int):
    try:
        qs = DetectionTask.objects.all() if request.user.is_staff else DetectionTask.objects.filter(created_by=request.user)
        t = qs.get(id=task_id)
    except DetectionTask.DoesNotExist:
        return Response({"detail": "任务不存在"}, status=404)
    t.status = 'processing'
    t.error_message = ''
    t.finished_at = None
    if getattr(t, 'annotated_file', None):
        t.annotated_file = None
    t.detections = []
    t.process_time_ms = 0
    if getattr(t, 'verify_status', None) is not None:
        t.verify_status = 'verified'
    if getattr(t, 'verify_result', None) is not None:
        t.verify_result = None
    t.save(update_fields=['status', 'error_message', 'finished_at', 'annotated_file', 'detections', 'process_time_ms', 'verify_status', 'verify_result'])
    th = threading.Thread(target=_process_detection_task, args=(t.id, t.confidence_threshold or 0.5), daemon=True)
    th.start()
    return Response({"detail": "已重新加入检测队列", "status": t.status}, status=202)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def task_verify(request, task_id: int):
    try:
        qs = DetectionTask.objects.all() if request.user.is_staff else DetectionTask.objects.filter(created_by=request.user)
        t = qs.get(id=task_id)
    except DetectionTask.DoesNotExist:
        return Response({"detail": "任务不存在"}, status=404)

    verify_status = (request.data.get("verify_status") or "").strip()
    allowed = {"pending", "verified"}
    if verify_status not in allowed:
        raise serializers.ValidationError({"verify_status": "无效的核实状态"})

    t.verify_status = verify_status
    verify_result = (request.data.get("verify_result") or "").strip()
    if verify_status == "pending":
        t.verify_result = None
    else:
        allowed_result = {"pass", "violation"}
        if verify_result not in allowed_result:
            raise serializers.ValidationError({"verify_result": "请提供核实结果"})
        t.verify_result = verify_result

    t.save(update_fields=["verify_status", "verify_result"])
    return Response({"id": t.id, "verify_status": _normalize_verify_status(t.verify_status), "verify_result": t.verify_result}, status=200)


def _floor_to_5min(dt):
    return dt.replace(minute=(dt.minute // 5) * 5, second=0, microsecond=0)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_trend(request):
    preset = (request.query_params.get("preset") or "1d").strip()
    if preset not in {"1h", "1d", "1w"}:
        preset = "1d"

    now = timezone.now()
    if preset == "1h":
        start = now - timedelta(hours=1)
    elif preset == "1w":
        start = now - timedelta(days=7)
    else:
        start = now - timedelta(days=1)

    qs = DetectionTask.objects.all() if request.user.is_staff else DetectionTask.objects.filter(created_by=request.user)
    qs = qs.filter(created_at__gte=start).only("id", "created_at", "verify_status", "detections")

    buckets = {}
    labels = []
    if preset == "1h":
        base = _floor_to_5min(timezone.localtime(now))
        for i in range(12):
            dt = base - timedelta(minutes=(11 - i) * 5)
            k = dt.strftime("%H:%M")
            labels.append(k)
            buckets[k] = {"ai_alerts": 0, "pending_verifications": 0}
    elif preset == "1d":
        base = timezone.localtime(now).replace(minute=0, second=0, microsecond=0)
        for i in range(24):
            dt = base - timedelta(hours=(23 - i))
            k = dt.strftime("%m-%d %H:00")
            labels.append(k)
            buckets[k] = {"ai_alerts": 0, "pending_verifications": 0}
    else:
        base = timezone.localtime(now).replace(hour=0, minute=0, second=0, microsecond=0)
        for i in range(7):
            dt = base - timedelta(days=(6 - i))
            k = dt.strftime("%m-%d")
            labels.append(k)
            buckets[k] = {"ai_alerts": 0, "pending_verifications": 0}

    def _has_violation(dets):
        if not isinstance(dets, list):
            return False
        for d in dets:
            if isinstance(d, dict) and int(d.get("cls", -1)) == 0:
                return True
        return False

    for t in qs:
        local_created = timezone.localtime(t.created_at)
        if preset == "1h":
            k = _floor_to_5min(local_created).strftime("%H:%M")
        elif preset == "1d":
            k = local_created.replace(minute=0, second=0, microsecond=0).strftime("%m-%d %H:00")
        else:
            k = local_created.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%m-%d")
        if k not in buckets:
            continue
        if _has_violation(t.detections):
            buckets[k]["ai_alerts"] += 1
        if _normalize_verify_status(getattr(t, "verify_status", "verified")) == "pending":
            buckets[k]["pending_verifications"] += 1

    ai = [buckets[k]["ai_alerts"] for k in labels]
    pending = [buckets[k]["pending_verifications"] for k in labels]
    return Response({"preset": preset, "labels": labels, "ai_alerts": ai, "pending_verifications": pending}, status=200)


def _frontend_base() -> str:
    return os.getenv("FRONTEND_BASE_URL", "http://localhost:5173").rstrip("/")


def _issue_share_token(task: DetectionTask, user) -> ShareLink:
    expires_at = timezone.now() + timedelta(days=7)
    for _ in range(5):
        token = secrets.token_urlsafe(18)
        if not ShareLink.objects.filter(token=token).exists():
            return ShareLink.objects.create(
                token=token,
                task=task,
                created_by=user,
                expires_at=expires_at,
            )
    raise RuntimeError("无法生成唯一分享令牌")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_share_create(request, task_id: int):
    try:
        qs = DetectionTask.objects.all() if request.user.is_staff else DetectionTask.objects.filter(created_by=request.user)
        t = qs.get(id=task_id)
    except DetectionTask.DoesNotExist:
        return Response({"detail": "任务不存在"}, status=404)
    if t.task_type != 'image':
        return Response({"detail": "仅支持图片任务生成分享链接"}, status=400)
    link = _issue_share_token(t, request.user)
    url = f"{_frontend_base()}/share/report?id={link.token}"
    return Response({"url": url, "expires_at": timezone.localtime(link.expires_at).isoformat()}, status=201)


@api_view(['GET'])
def share_report(request):
    token = request.query_params.get("id") or request.query_params.get("token") or ""
    token = token.strip()
    if not token:
        return Response({"detail": "缺少分享令牌"}, status=400)
    try:
        link = ShareLink.objects.select_related("task").get(token=token)
    except ShareLink.DoesNotExist:
        return Response({"detail": "分享链接无效"}, status=404)
    if link.revoked or link.is_expired():
        return Response({"detail": "分享链接已失效"}, status=410)
    t = link.task
    if t.task_type != 'image':
        return Response({"detail": "该分享仅支持图片报告"}, status=400)
    dets = t.detections or []
    viol_confs = []
    if isinstance(dets, list):
        for d in dets:
            if isinstance(d, dict) and int(d.get("cls", -1)) == 0:
                try:
                    viol_confs.append(float(d.get("conf", 0.0)))
                except Exception:
                    pass
    violation_confidence = max(viol_confs) if viol_confs else 0.0
    rec = SmokingRecord.objects.filter(task=t).order_by("-detected_at").first()
    llm_report = (rec.llm_report or "") if rec else ""
    data = {
        "task_id": t.id,
        "name": t.task_name,
        "created_at": timezone.localtime(t.created_at).strftime('%Y-%m-%d %H:%M:%S'),
        "source_url": request.build_absolute_uri(t.file_path.url) if hasattr(t.file_path, 'url') else str(t.file_path),
        "detections": dets if isinstance(dets, list) else [],
        "violation_confidence": violation_confidence,
        "llm_report": llm_report,
    }
    return Response(data, status=200)


# 6. 自定义：使用邮箱(email)登录获取 JWT
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    使用 email + password 登录：
    - 前端传入 { "email": "xxx@xx.com", "password": "xxx" }
    - 这里根据 email 找到对应用户，再走原有 JWT 流程
    """
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("邮箱和密码不能为空")

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("账号或密码不正确")

        # 调用父类逻辑时，仍然用用户名(username)去认证
        data = {"username": user.get_username(), "password": password}
        return super().validate(data)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all().order_by('-created_at')
    serializer_class = CameraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        search = (self.request.query_params.get('search') or '').strip()
        if search:
            qs = qs.filter(models.Q(name__icontains=search) | models.Q(region__icontains=search))
        return qs

    def perform_create(self, serializer):
        serializer.save(is_online=False, last_active=None)

    def perform_update(self, serializer):
        serializer.save(is_online=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def camera_upload_file(request):
    upload = request.FILES.get('file')
    if not upload:
        return Response({'detail': '未收到上传文件'}, status=400)

    ext = os.path.splitext(upload.name or '')[1].lower()
    if ext not in {'.mp4', '.avi', '.mov', '.mkv', '.webm'}:
        return Response({'detail': '仅支持 MP4、AVI、MOV、MKV、WEBM 视频文件'}, status=400)

    relative_dir = os.path.join('uploads', 'camera-files')
    absolute_dir = os.path.join(settings.MEDIA_ROOT, relative_dir)
    os.makedirs(absolute_dir, exist_ok=True)

    safe_name = f"{timezone.now().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(4)}{ext}"
    relative_path = os.path.join(relative_dir, safe_name)
    absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    with open(absolute_path, 'wb+') as destination:
        for chunk in upload.chunks():
            destination.write(chunk)

    return Response({
        'detail': '上传成功',
        'relative_path': relative_path.replace('\\', '/'),
    }, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cameras_stats(request):
    qs = Camera.objects.all()
    total_count = qs.count()
    serialized = CameraSerializer(qs, many=True).data
    online_count = sum(1 for item in serialized if item.get('effective_is_online'))
    offline_count = max(total_count - online_count, 0)
    return Response({
        'total_count': total_count,
        'online_count': online_count,
        'offline_count': offline_count,
        'alert_count': 0,
    }, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cameras_grouped(request):
    qs = Camera.objects.all().order_by('region', '-created_at')
    groups = []
    region_map = {}
    for camera in qs:
        region = camera.region or '未分组'
        if region not in region_map:
            region_map[region] = []
            groups.append({'region': region, 'items': region_map[region]})
        region_map[region].append(CameraSerializer(camera).data)
    return Response({'results': groups}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cameras_suggestions(request):
    qs = Camera.objects.all().order_by('-last_active', '-updated_at', '-created_at')[:5]
    return Response({'results': CameraSerializer(qs, many=True).data}, status=200)


class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all().order_by('-updated_at', '-created_at')
    serializer_class = AIModelSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def llm_service_overview(request):
    return Response(_build_llm_overview_payload(), status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def llm_service_list(request):
    _ensure_llm_service_defaults()
    services = LLMServiceConfig.objects.all().order_by('sort_order', 'id')
    return Response({'results': LLMServiceListSerializer(services, many=True).data}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def llm_service_models(request, service_key: str):
    _ensure_llm_service_defaults()
    try:
        service = LLMServiceConfig.objects.get(service_key=service_key)
    except LLMServiceConfig.DoesNotExist:
        return Response({'detail': '服务商不存在'}, status=404)
    models = [
        {
            'value': name,
            'label': name,
            'category': _get_model_category(name),
        }
        for name in (service.model_options or [])
    ]
    return Response({
        'service_key': service.service_key,
        'service_name': service.service_name,
        'models': models,
        'base_url': service.base_url,
        'api_key_url': service.api_key_url,
        'current_model': service.model_name or '',
        'has_api_key': bool((service.api_key or '').strip()),
        'masked_api_key': _mask_api_key(service.api_key or ''),
        'request_timeout': service.request_timeout or 30,
        'enabled': service.enabled,
    }, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def llm_current_config(request):
    payload = _build_llm_overview_payload()
    return Response(payload.get('current_config') or {}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def llm_service_save(request):
    _ensure_llm_service_defaults()
    serializer = LLMServiceSaveSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    service = LLMServiceConfig.objects.get(service_key=data['service_key'])

    if data.get('enabled'):
        LLMServiceConfig.objects.exclude(id=service.id).update(enabled=False)

    service.model_name = data['model_name']
    service.api_key = data['api_key']
    service.request_timeout = data.get('request_timeout', service.request_timeout or 30)
    service.enabled = bool(data.get('enabled', False))
    service.save(update_fields=['model_name', 'api_key', 'request_timeout', 'enabled', 'updated_at'])
    _sync_active_llm_model(service, request.user)
    return Response({
        'detail': '配置保存成功',
        'service': LLMServiceDetailSerializer(service).data,
        'overview': _build_llm_overview_payload(),
    }, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def llm_service_test(request):
    _ensure_llm_service_defaults()
    service_key = (request.data.get('service_key') or '').strip()
    if not service_key:
        return Response({'detail': '缺少服务商标识'}, status=400)
    try:
        service = LLMServiceConfig.objects.get(service_key=service_key)
    except LLMServiceConfig.DoesNotExist:
        return Response({'detail': '服务商不存在'}, status=404)

    api_key = request.data.get('api_key')
    model_name = request.data.get('model_name')
    ok, message = _test_llm_service_connection(service, api_key=api_key, model_name=model_name)
    service.is_connected = ok
    service.last_tested_at = timezone.now()
    service.save(update_fields=['is_connected', 'last_tested_at', 'updated_at'])
    return Response({
        'success': ok,
        'message': message,
        'service_key': service.service_key,
        'tested_at': timezone.localtime(service.last_tested_at).isoformat() if service.last_tested_at else '',
    }, status=200 if ok else 400)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def llm_service_switch(request):
    _ensure_llm_service_defaults()
    serializer = LLMServiceSwitchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    service = serializer.instance
    LLMServiceConfig.objects.exclude(id=service.id).update(enabled=False)
    service.enabled = True
    service.save(update_fields=['enabled', 'updated_at'])
    _sync_active_llm_model(service, request.user)
    return Response({
        'detail': f'已切换到 {service.service_name}',
        'service': LLMServiceDetailSerializer(service).data,
        'overview': _build_llm_overview_payload(),
    }, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def active_model_config(request):
    config = ActiveModelConfig.objects.order_by('id').first()
    if not config:
        return Response({
            'detection_model': None,
            'llm_model': None,
            'inference_threshold': 0.75,
            'response_mode': '自动分析',
            'deploy_node': '',
        }, status=200)
    return Response(ActiveModelConfigSerializer(config).data, status=200)


@api_view(['POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_active_model_config(request):
    config = ActiveModelConfig.objects.order_by('id').first()
    if not config:
        config = ActiveModelConfig.objects.create()
    serializer = ActiveModelConfigSerializer(config, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save(updated_by=request.user)
    return Response(ActiveModelConfigSerializer(config).data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def camera_preview_stream(request):
    return Response({'detail': '预览流功能暂未恢复'}, status=501)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def camera_stream(request, pk: int):
    return Response({'detail': f'摄像头 {pk} 实时流功能暂未恢复'}, status=501)
