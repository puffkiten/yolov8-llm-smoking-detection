import requests

url = "http://127.0.0.1:8000/api/login/"
# 🚨 把这里的 username 和 password 换成你刚才 createsuperuser 设置的老板账号！
data = {
    "username": "yosh",
    "password": "123456"
}

print("🚀 正在模拟前端发送登录请求...")
response = requests.post(url, data=data)

print("\n========== 🎯 后端返回的登录结果 ==========")
print(response.json())