# 22-2project

前后端分离项目：
- 前端：Vue 3 + Vite（目录：`frontend/`）
- 后端：Django + DRF（目录：`backend/`）

## 1. 环境要求

- Node.js：建议 `20+`
- Python：固定使用 `3.11.x`（不要使用 `3.13`）
- 数据库：PostgreSQL（由 `backend/.env` 配置）

## 2. 快速启动

### 2.1 启动后端（Django）

推荐直接使用项目根目录现成的 `/.venv311`，或重新用 Python 3.11 创建 `backend/.venv`。

```bash
cd /Users/yosh/Documents/22-2project
source .venv311/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py runserver 0.0.0.0:8000
```

如果你更希望把虚拟环境放在 `backend/.venv`：

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

后端默认监听：`http://0.0.0.0:8000`

### 2.2 启动前端（Vue）

```bash
cd frontend
npm install
npm run dev
```

前端默认地址：`http://localhost:5173`

前端 API 基址通过环境变量配置：

```bash
cp frontend/.env.example frontend/.env.local
```

`frontend/.env.local` 示例：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## 3. 环境变量配置

1. 复制模板：

```bash
cp backend/.env.example backend/.env
```

2. 按需填写关键项：
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT`
- 邮件和第三方登录相关变量（如启用）

## 4. 常见问题

### 4.1 `No module named 'django'`

通常是未激活虚拟环境或依赖未安装：

```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
```

### 4.2 `python manage.py runserver` 报 torch/ultralytics 相关错误

这通常是 Python 版本不对或虚拟环境混用了 `3.13`。请固定使用 Python `3.11.x`，并重建虚拟环境后重装依赖。

推荐直接使用项目根目录的 `/.venv311`：

```bash
cd /Users/yosh/Documents/22-2project
source .venv311/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py runserver
```

### 4.3 `ERROR: No matching distribution found for Django<7,>=6.0`

这是 Python 版本与 Django 版本约束不匹配导致。当前项目建议组合：
- Python `3.11`
- Django `5.2.x`

请确保在 `backend/.venv` 激活后再安装依赖。

### 4.4 仍然请求到旧的 API 地址

前端已改为读取 `VITE_API_BASE_URL`，修改后需要重启前端开发服务：

```bash
cd frontend
npm run dev
```

## 5. 安全与仓库规范

- 不要提交真实 `.env` 文件或密钥
- 不要提交虚拟环境目录（如 `.venv/`）
- 不要提交本地数据库与媒体运行文件（如 `db.sqlite3`、`media/`）
