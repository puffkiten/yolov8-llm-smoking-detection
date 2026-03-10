import requests

# 🚨 确保你刚才测试用的那张 test_pen.jpg 就在 22-2project 目录下！
image_path = "test_qw.jpg"

url = "http://127.0.0.1:8000/api/detect/"

print("🚀 正在向你的 Django 服务器发送图片...")
try:
    with open(image_path, 'rb') as f:
        # 把图片打包成表单数据，名字叫 'image' (后端刚好在等这个名字)
        files = {'image': f}
        # 发射 POST 请求！
        response = requests.post(url, files=files)

    print("\n========== 🎯 后端返回的完整 JSON 结果 ==========")
    print(response.json())
except FileNotFoundError:
    print(f"❌ 找不到图片文件：{image_path}，请检查图片是不是放在这儿了！")
except Exception as e:
    print(f"❌ 请求失败，错误信息：{e}")