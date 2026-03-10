import base64
from openai import OpenAI

# 1. 填入你刚刚在阿里云百炼复制的 API Key
# 🚨 记得替换成你自己的！
API_KEY = "sk-684b162505a2494fb27c6848399c6c85"

# 2. 行业标准写法：用 OpenAI 的壳，连阿里的芯
client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 指向阿里云百炼服务器
)


def encode_image_to_base64(image_path):
    """把图片变成大模型认识的 Base64 长文本"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_image_for_smoking(image_path):
    print("🧠 正在连线阿里通义千问大脑，请求分析中...")
    base64_img = encode_image_to_base64(image_path)

    try:
        # 调用 Qwen-VL-Plus (阿里的视觉多模态主力模型)
        # type: ignore
        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "你是一个严谨的安防质检员。请仔细观察这张图片，画面中的人员是否在吸烟？请重点辨别他嘴里的物品是香烟还是其他干扰物（如笔、木棍、吸管等）。请给出明确的结论，并简要说明判断依据（是否有烟雾特征、物品颜色等）。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_img}"
                            }
                        }
                    ]
                }
            ]
        )

        # 打印大模型经过思考后得出的结论
        result_text = response.choices[0].message.content
        print("\n================ ⚡ 阿里 AI 复合研判报告 ================")
        print(result_text)
        print("=======================================================\n")

    except Exception as e:
        print(f"❌ 大模型调用失败: {e}")


if __name__ == '__main__':
    # 找一张你叼着笔或者真抽烟的照片测试一下
    test_image_path = "test_qw.jpg"  # 确保当前目录下有这张图
    analyze_image_for_smoking(test_image_path)