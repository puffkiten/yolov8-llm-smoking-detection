# 文件位置：backend/ai_core/llm_agent.py
import base64
from openai import OpenAI

# 🚨 换成你自己的阿里 API KEY
API_KEY = "sk-684b162505a2494fb27c6848399c6c85"
client = OpenAI(api_key=API_KEY, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")


def analyze_smoking(image_path):
    """供 Django 调用的复核函数：传入图片路径，返回大模型的一段话结论"""
    with open(image_path, "rb") as image_file:
        base64_img = base64.b64encode(image_file.read()).decode('utf-8')

    try:
        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": "你是一个严谨的安防质检员。请仔细观察图片，画面中的人员是否在吸烟？请重点辨别他嘴里或手里的是香烟还是其他干扰物（如笔、木棍）。请直接给出明确结论和简要依据。"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                    ]
                }
            ]
        )
        return response.choices[0].message.content  # 这里的 return 是重点！
    except Exception as e:
        return f"AI 辅助分析失败: {str(e)}"