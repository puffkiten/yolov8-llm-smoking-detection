from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Aero Smart API")

# 配置允许跨域请求（极其重要！否则你的 Vue 连不上后端）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:5174", # 👈 加上你的新地址
        "http://127.0.0.1:5174"
    ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Aero Smart Backend Engine!"}

@app.get("/api/status")
async def get_status():
    return {
        "status": "Running",
        "model": "YOLOv8-Smoking-v2",
        "active_cameras": 4
    }

# 启动服务器的入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)