from django.shortcuts import render

# Create your views here.
# 文件位置：backend/detection/views.py
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ultralytics import YOLO
from ai_core.llm_agent import analyze_smoking

# 1. 启动时加载 YOLO 模型 (只加载一次，提高速度)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ai_core', 'best.pt')
model = YOLO(MODEL_PATH)


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