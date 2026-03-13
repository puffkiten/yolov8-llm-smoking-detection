# 文件位置：backend/ai_core/llm_agent.py
import base64
import os
from openai import OpenAI
from pathlib import Path

API_KEY = os.getenv("DASHSCOPE_API_KEY", "") or os.getenv("QWEN_API_KEY", "")
# 后备：尝试读取项目根目录 llm_agent.py 里的 API_KEY
if not API_KEY:
    try:
        from django.conf import settings
        import sys
        root_dir = Path(settings.BASE_DIR).parent
        if str(root_dir) not in sys.path:
            sys.path.append(str(root_dir))
        import llm_agent as external
        API_KEY = getattr(external, "API_KEY", "") or ""
    except Exception:
        pass
client = OpenAI(api_key=API_KEY, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

def _detect_image_mime(raw: bytes) -> str:
    if raw.startswith(b"\xFF\xD8\xFF"):
        return "image/jpeg"
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if raw.startswith(b"GIF87a") or raw.startswith(b"GIF89a"):
        return "image/gif"
    if raw.startswith(b"RIFF") and raw[8:12] == b"WEBP":
        return "image/webp"
    if raw.startswith(b"BM"):
        return "image/bmp"
    if raw.startswith(b"II*\x00") or raw.startswith(b"MM\x00*"):
        return "image/tiff"
    return ""


def analyze_smoking(image_path):
    """供 Django 调用的复核函数：传入图片路径，返回大模型的一段话结论"""
    if not API_KEY:
        return "AI 辅助分析失败: 未配置 DASHSCOPE_API_KEY/QWEN_API_KEY"
    with open(image_path, "rb") as image_file:
        raw = image_file.read()

    mime = _detect_image_mime(raw)
    if not mime:
        return "AI 辅助分析失败: 文件不是可识别的图片格式"
    base64_img = base64.b64encode(raw).decode("utf-8")

    try:
        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": "你是一个严谨的安防质检员。请仔细观察图片，画面中的人员是否在吸烟？请重点辨别他嘴里或手里的是香烟还是其他干扰物（如笔、木棍）。请直接给出明确结论和简要依据。"},
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{base64_img}"}}
                    ]
                }
            ]
        )
        return response.choices[0].message.content  # 这里的 return 是重点！
    except Exception as e:
        return f"AI 辅助分析失败: {str(e)}"
