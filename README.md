# Aero Smart

Aero Smart 是一个面向吸烟行为识别与监控管理场景的前后端分离项目，覆盖了从摄像头接入、实时监控、图片/视频检测任务、人工核实，到大模型服务配置的完整业务链路。

项目当前采用：

- 前端：Vue 3 + Vite + Element Plus
- 后端：Django + Django REST Framework
- 检测引擎：YOLO / Ultralytics
- 大模型接入：兼容 OpenAI 风格接口的多服务商配置
- 数据库：PostgreSQL

## 1. 项目能力

### 1.1 核心业务模块

- 实时监控矩阵
  - 摄像头列表与激活监控
  - MJPEG 实时流展示
  - 实时 YOLO 目标框与置信度叠加
- 检测任务中心
  - 图片检测任务上传
  - 视频检测任务上传
  - 任务结果查看
  - 人工核实与状态流转
- 摄像头配置中心
  - 新增/编辑/删除摄像头
  - 支持流地址或本地录像文件接入
  - 置信度阈值配置
- AI 模型与大模型管理
  - 当前检测模型展示
  - 多家大模型服务商配置与切换
  - API Key 管理与连通性测试
- 认证与账号能力
  - JWT 登录
  - 注册 / 忘记密码 / 重置密码
  - Google 登录流程页面
- 分享与导出
  - 检测任务结果分享
  - 任务记录导出

### 1.2 当前仓库特征

本仓库同时包含：

- 业务前后端源码
- YOLO 模型文件与训练产物目录
- 本地测试脚本与示例数据

因此它既可以作为业务系统仓库使用，也保留了一定的模型训练/调试痕迹。

## 2. 技术架构

### 2.1 前端

目录：`frontend/`

技术栈：

- Vue `3.5.x`
- Vite `7.x`
- Element Plus `2.x`
- Axios
- Vue Router
- Pinia
- ECharts

前端主要页面：

- `src/views/Dashboard.vue`：仪表板
- `src/views/camera/Config.vue`：摄像头配置
- `src/views/camera/Realtime.vue`：实时监控
- `src/views/detection/Upload.vue`：发起检测
- `src/views/detection/Tasks.vue`：检测任务
- `src/views/system/AIModelManage.vue`：AI 模型管理
- `src/views/system/UserManage.vue`：用户管理

### 2.2 后端

目录：`backend/`

技术栈：

- Django `5.2.x`
- Django REST Framework
- Simple JWT
- psycopg2
- OpenCV
- Ultralytics
- OpenAI Python SDK

后端主要模块：

- `backend/backend/`：Django 配置
- `backend/detection/`：核心业务应用
- `backend/ai_core/`：检测模型与大模型分析封装

### 2.3 数据与模型

- YOLO 权重文件：`backend/ai_core/best.pt`
- 训练相关目录：`runs/`、`datasets/`
- 任务结果、截图、媒体文件：运行时保存在 Django `MEDIA_ROOT`

## 3. 目录结构

```text
22-2project/
├── backend/
│   ├── ai_core/
│   ├── backend/
│   ├── detection/
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── router/
│   │   ├── styles/
│   │   ├── utils/
│   │   └── views/
│   ├── package.json
│   └── .env.example
├── datasets/
├── runs/
├── README.md
└── .python-version
```

## 4. 运行环境要求

### 4.1 基础环境

- Node.js：`20+`
- Python：`3.11.x`
- PostgreSQL：`14+` 或兼容版本
- 推荐系统：macOS / Linux

### 4.2 为什么固定 Python 3.11

当前仓库依赖 Django、OpenCV、Ultralytics 等组件，Python `3.11` 的兼容性最稳定。

不建议直接使用 Python `3.13` 运行本项目。

## 5. 快速开始

## 5.1 克隆项目

```bash
git clone <your-repo-url>
cd 22-2project
```

## 5.2 配置后端环境变量

复制模板：

```bash
cp backend/.env.example backend/.env
```

至少需要正确填写：

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `FRONTEND_BASE_URL`

如需大模型分析，还需要配置至少一个可用服务商的 Key，例如：

- `DASHSCOPE_API_KEY`
- `QWEN_API_KEY`

## 5.3 启动后端

仓库中已经存在一个常用虚拟环境路径示例：`/.venv311`。

方式一：直接使用现有 Python 3.11 虚拟环境

```bash
source .venv311/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py runserver 0.0.0.0:8000
```

方式二：自行创建新的虚拟环境

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

后端默认地址：

- `http://127.0.0.1:8000`

## 5.4 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端默认地址：

- `http://localhost:5173`

## 5.5 配置前端 API 地址

复制模板：

```bash
cp frontend/.env.example frontend/.env.local
```

默认内容：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

修改后需要重启前端开发服务。

## 6. 开发流程建议

### 6.1 常用本地启动顺序

1. 启动 PostgreSQL
2. 启动 Django 后端
3. 启动 Vue 前端
4. 登录系统后验证：
   - 摄像头配置
   - 实时监控
   - 检测任务上传
   - AI 模型管理

### 6.2 数据库迁移

```bash
python backend/manage.py makemigrations
python backend/manage.py migrate
```

### 6.3 创建管理员账号

```bash
python backend/manage.py createsuperuser
```

## 7. 关键接口与业务说明

### 7.1 检测任务

相关接口：

- `POST /api/detection/upload`
- `GET /api/detection/tasks`
- `GET /api/detection/tasks/<task_id>`
- `POST /api/detection/tasks/<task_id>/retry`
- `PATCH /api/detection/tasks/<task_id>/verify`

支持：

- 图片上传检测
- 视频上传检测
- 任务结果查看
- 人工核实状态流转

### 7.2 摄像头管理

相关接口：

- `GET /api/cameras/`
- `POST /api/cameras/`
- `PATCH /api/cameras/<id>/`
- `DELETE /api/cameras/<id>/`
- `GET /api/cameras/grouped/`
- `GET /api/cameras/stats/`
- `GET /api/cameras/<id>/stream/`

### 7.3 大模型服务配置

相关接口：

- `GET /api/llm-services/overview`
- `GET /api/llm-services/<service_key>/models`
- `POST /api/llm-services/test`
- `POST /api/llm-services/save`
- `POST /api/llm-services/switch`

## 8. 部署建议

### 8.1 后端部署

生产环境建议：

- Gunicorn / Uvicorn + Nginx
- 独立 PostgreSQL 实例
- 媒体目录单独挂载
- 模型文件与训练产物放置在稳定磁盘路径

### 8.2 前端部署

生产环境建议：

```bash
cd frontend
npm run build
```

将 `dist/` 部署到 Nginx 或静态资源服务器。

### 8.3 媒体与模型文件

请注意以下目录在生产环境中通常体积较大：

- `backend/ai_core/best.pt`
- `runs/`
- `datasets/`
- `media/`（运行时生成）

如果仓库后续需要收敛为纯业务交付版本，建议将训练数据与训练结果拆分到独立存储。

## 9. 常见问题

### 9.1 前端请求失败或登录后跳回登录页

优先检查：

- `VITE_API_BASE_URL` 是否正确
- 后端是否已启动
- 浏览器本地 Token 是否过期

### 9.2 视频流黑屏

优先检查：

- 摄像头流地址是否可访问
- 本地录像文件是否存在
- 后端是否能正常读取媒体文件
- 实时流接口是否已被当前环境允许访问

### 9.3 YOLO / OpenCV 依赖安装失败

优先检查：

- Python 是否为 `3.11`
- 虚拟环境是否激活
- 是否在正确目录执行 `pip install -r backend/requirements.txt`

### 9.4 大模型分析没有结果

优先检查：

- 大模型服务是否已配置 API Key
- 当前启用的大模型服务是否测试连接成功
- 上传任务是否真的检测到目标

## 10. 安全与仓库规范

- 不要提交真实 `.env`
- 不要提交生产密钥、API Key、数据库密码
- 不要提交本地虚拟环境目录
- 不要将生产媒体文件直接纳入版本控制

建议保留：

- `.env.example`
- 必要的模型配置模板
- 必要的初始化脚本与迁移文件

## 11. 后续建议

如果项目后续需要用于正式展示或交付，建议进一步补充：

- 接口文档（OpenAPI / Swagger）
- Docker Compose 一键启动
- CI/CD 流程
- 测试用例与回归清单
- 更明确的媒体文件与训练产物管理策略

---

如需在新的机器上复现环境，推荐优先完成以下 4 步：

1. 安装 Python 3.11 与 Node.js 20+
2. 配置 PostgreSQL 与 `backend/.env`
3. 启动 Django 后端
4. 启动 Vue 前端并验证核心页面链路
