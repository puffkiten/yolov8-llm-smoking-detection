# backend/detection/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 兼容处理：获取前端传过来的 email 或 username
        email = kwargs.get('email', username)
        
        if not email:
            return None
            
        try:
            # 1. 先尝试去邮箱列（email）里找
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            try:
                # 2. 如果邮箱没找到，再尝试去用户名列（username）里找
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                return None
                
        # 如果找到了用户，校验密码是否正确
        if user.check_password(password):
            return user
            
        return None