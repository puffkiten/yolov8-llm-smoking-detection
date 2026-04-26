import json
import os
import smtplib
import urllib.parse
import urllib.request
from email.message import EmailMessage

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


token_generator = PasswordResetTokenGenerator()


def _frontend_base_url() -> str:
    # 允许通过环境变量配置前端地址；默认本地 Vite
    return os.getenv("FRONTEND_BASE_URL", "http://localhost:5173").rstrip("/")


def _send_email(to_email: str, subject: str, body: str) -> None:
    host = getattr(settings, "EMAIL_HOST", "") or ""
    user = getattr(settings, "EMAIL_HOST_USER", "") or ""
    password = getattr(settings, "EMAIL_HOST_PASSWORD", "") or ""
    port = int(getattr(settings, "EMAIL_PORT", 587) or 587)
    timeout = int(getattr(settings, "EMAIL_TIMEOUT", 10) or 10)
    use_ssl = bool(getattr(settings, "EMAIL_USE_SSL", False))
    use_tls = bool(getattr(settings, "EMAIL_USE_TLS", False))
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or user

    if not host or not user or not password or not from_email:
        raise RuntimeError("SMTP 未配置完整")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    attempts = []
    attempts.append(("ssl" if use_ssl else "tls" if use_tls else "plain", port))
    if host == "smtp.gmail.com":
        if port == 587:
            attempts.append(("ssl", 465))
        elif port == 465:
            attempts.append(("tls", 587))

    last_exc = None
    for mode, p in attempts:
        try:
            if mode == "ssl":
                server = smtplib.SMTP_SSL(host, p, timeout=timeout)
                server.ehlo()
            else:
                server = smtplib.SMTP(host, p, timeout=timeout)
                server.ehlo()
                if mode == "tls":
                    server.starttls()
                    server.ehlo()
            server.login(user, password)
            server.send_message(msg)
            server.quit()
            return
        except Exception as exc:
            last_exc = exc
            try:
                server.quit()
            except Exception:
                pass

    raise last_exc or RuntimeError("SMTP 发送失败")


@api_view(["POST"])
def password_reset_request(request):
    """
    忘记密码（请求重置）
    入参: { "email": "xxx@xx.com" }

    说明：
    - 通过邮箱发送重置链接
    """
    email = (request.data.get("email") or "").strip()
    if not email:
        return Response({"detail": "请输入邮箱"}, status=status.HTTP_400_BAD_REQUEST)

    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"detail": "该邮箱未注册"}, status=status.HTTP_400_BAD_REQUEST)

    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    reset_url = f"{_frontend_base_url()}/reset-password?uid={uidb64}&token={urllib.parse.quote(token)}"

    subject = "Aero Smart 重置密码"
    message = f"请点击以下链接重置密码：\n\n{reset_url}\n\n如果不是你本人操作，请忽略此邮件。"

    try:
        _send_email(email, subject, message)
    except Exception as exc:
        if getattr(settings, "DEBUG", False):
            return Response({"detail": f"邮件发送失败：{exc.__class__.__name__}: {str(exc)}"}, status=500)
        return Response({"detail": "邮件发送失败，请检查邮箱 SMTP 配置"}, status=500)

    return Response({"detail": "重置邮件已发送，请查收"}, status=200)


@api_view(["POST"])
def password_reset_confirm(request):
    """
    忘记密码（确认重置）
    入参: { "uid": "...", "token": "...", "new_password": "..." }
    """
    uidb64 = request.data.get("uid")
    token = request.data.get("token")
    new_password = request.data.get("new_password")

    if not uidb64 or not token or not new_password:
        return Response({"detail": "参数不完整"}, status=status.HTTP_400_BAD_REQUEST)
    if len(new_password) < 6:
        return Response({"detail": "密码至少 6 位"}, status=status.HTTP_400_BAD_REQUEST)

    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        return Response({"detail": "链接无效或已过期"}, status=status.HTTP_400_BAD_REQUEST)

    if not token_generator.check_token(user, token):
        return Response({"detail": "链接无效或已过期"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save(update_fields=["password"])

    return Response({"detail": "密码已重置，请使用新密码登录"}, status=200)


def _google_client_config():
    # 默认值使用用户提供的 Client ID
    default_id = "1023668174872-jg6vs23283r4h884dt2v4vfs05jugptf.apps.googleusercontent.com"
    client_id = os.getenv("GOOGLE_CLIENT_ID", default_id)
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
    return client_id, client_secret


@api_view(["GET"])
def google_login(request):
    """
    发起 Google OAuth（浏览器跳转）
    """
    client_id, _ = _google_client_config()
    if not client_id:
        return Response(
            {"detail": "未配置 GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET"},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )

    redirect_uri = f"http://127.0.0.1:8000/api/auth/google/callback"
    state = request.query_params.get("state", "aero")

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect(auth_url)


def _http_post_json(url: str, data: dict) -> dict:
    payload = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _http_get_json(url: str, headers: dict) -> dict:
    req = urllib.request.Request(url, method="GET")
    for k, v in headers.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


@api_view(["GET"])
def google_callback(request):
    """
    Google OAuth 回调：
    - 支持用 code 换 access_token (Authorization Code Flow)
    - 或者直接接收 access_token (Implicit Flow / Popup Flow)
    - 拉取用户信息
    - 创建/绑定本系统用户
    - 签发本系统 JWT（refresh/access）
    - 跳回前端 /auth/google/callback 携带 token
    """
    code = request.query_params.get("code")
    access_token = request.query_params.get("access_token")

    if not code and not access_token:
        return Response({"detail": "缺少 code 或 access_token"}, status=status.HTTP_400_BAD_REQUEST)

    client_id, client_secret = _google_client_config()

    if code:
        # Authorization Code Flow: 用 code 换 access_token
        if not client_id or not client_secret:
            return Response(
                {"detail": "未配置 GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET，无法使用 code 换取 token"},
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

        redirect_uri = f"http://127.0.0.1:8000/api/auth/google/callback"
        token_resp = _http_post_json(
            "https://oauth2.googleapis.com/token",
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            },
        )
        access_token = token_resp.get("access_token")
        if not access_token:
            return Response({"detail": "Google token 交换失败", "raw": token_resp}, status=400)

    # 统一使用 access_token 获取用户信息
    userinfo = _http_get_json(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        {"Authorization": f"Bearer {access_token}"},
    )

    email = userinfo.get("email")
    if not email:
        return Response({"detail": "无法获取 Google 邮箱", "raw": userinfo}, status=400)

    User = get_user_model()
    user, created = User.objects.get_or_create(email=email, defaults={"username": email.split("@")[0]})
    if created:
        # 如果 username 冲突，做一个简单的兜底
        base = user.username
        i = 1
        while User.objects.filter(username=user.username).exclude(pk=user.pk).exists():
            user.username = f"{base}{i}"
            i += 1
        user.set_unusable_password()
        user.save()

    refresh = RefreshToken.for_user(user)
    frontend_cb = f"{_frontend_base_url()}/auth/google/callback?access={urllib.parse.quote(str(refresh.access_token))}&refresh={urllib.parse.quote(str(refresh))}"

    # 用 302 跳回前端
    from django.http import HttpResponseRedirect

    return HttpResponseRedirect(frontend_cb)


@api_view(["POST"])
def register(request):
    """
    用户注册
    入参: { "email": "...", "username": "...", "password": "..." }
    返回: 201 + 用户基本信息
    """
    email = (request.data.get("email") or "").strip()
    username = (request.data.get("username") or "").strip()
    password = (request.data.get("password") or "").strip()

    if not email or not username or not password:
        return Response({"detail": "请填写邮箱、用户名和密码"}, status=status.HTTP_400_BAD_REQUEST)
    if len(password) < 6:
        return Response({"detail": "密码至少 6 位"}, status=status.HTTP_400_BAD_REQUEST)

    User = get_user_model()
    if User.objects.filter(email=email).exists():
        return Response({"detail": "该邮箱已被注册"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({"detail": "该用户名已被占用"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(username=username, email=email)
    user.set_password(password)
    user.save()

    data = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_staff": user.is_staff,
        "date_joined": getattr(user, "date_joined", None),
    }
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    """
    当前登录用户信息
    需在请求头携带 Authorization: Bearer <access_token>
    """
    user = request.user
    data = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_staff": user.is_staff,
    }
    return Response(data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def users_list(request):
    """
    用户列表（简版）
    需在请求头携带 Authorization: Bearer <access_token>
    """
    User = get_user_model()
    items = []
    for u in User.objects.all().order_by("id"):
        items.append({
            "id": u.id,
            "email": u.email,
            "username": u.username,
            "is_staff": u.is_staff,
            "is_active": u.is_active,
            "date_joined": getattr(u, "date_joined", None),
        })
    return Response({"results": items}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def users_create(request):
    if not request.user.is_staff:
        raise PermissionDenied("仅管理员可新增用户")

    email = (request.data.get("email") or "").strip()
    username = (request.data.get("username") or "").strip()
    password = (request.data.get("password") or "").strip()
    is_staff = bool(request.data.get("is_staff", False))
    is_active = bool(request.data.get("is_active", True))

    if not email or not username or not password:
        return Response({"detail": "请填写邮箱、用户名和密码"}, status=status.HTTP_400_BAD_REQUEST)
    if len(password) < 6:
        return Response({"detail": "密码至少 6 位"}, status=status.HTTP_400_BAD_REQUEST)

    User = get_user_model()
    if User.objects.filter(email=email).exists():
        return Response({"detail": "该邮箱已被注册"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({"detail": "该用户名已被占用"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(username=username, email=email, is_staff=is_staff, is_active=is_active)
    user.set_password(password)
    user.save()

    return Response({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "date_joined": getattr(user, "date_joined", None),
    }, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def users_update(request, user_id: int):
    if not request.user.is_staff:
        raise PermissionDenied("仅管理员可编辑用户")

    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"detail": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

    username = request.data.get("username")
    email = request.data.get("email")
    is_staff = request.data.get("is_staff")
    is_active = request.data.get("is_active")
    password = (request.data.get("password") or "").strip()

    if username is not None:
        username = str(username).strip()
        if not username:
            return Response({"detail": "用户名不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            return Response({"detail": "该用户名已被占用"}, status=status.HTTP_400_BAD_REQUEST)
        user.username = username

    if email is not None:
        email = str(email).strip()
        if not email:
            return Response({"detail": "邮箱不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            return Response({"detail": "该邮箱已被注册"}, status=status.HTTP_400_BAD_REQUEST)
        user.email = email

    if is_staff is not None:
        user.is_staff = bool(is_staff)

    if is_active is not None:
        if user.pk == request.user.pk and not bool(is_active):
            return Response({"detail": "不能禁用当前登录账号"}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = bool(is_active)

    if password:
        if len(password) < 6:
            return Response({"detail": "密码至少 6 位"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)

    user.save()
    return Response({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "date_joined": getattr(user, "date_joined", None),
    }, status=200)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def users_delete(request, user_id: int):
    if not request.user.is_staff:
        raise PermissionDenied("仅管理员可删除用户")

    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"detail": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

    if user.pk == request.user.pk:
        return Response({"detail": "不能删除当前登录账号"}, status=status.HTTP_400_BAD_REQUEST)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
