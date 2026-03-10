from ultralytics import YOLO


def start_training():
    # 1. 加载基础模型
    model = YOLO("yolov8n.pt")

    print("🔥 检测到 Apple M4 Pro，启动 Metal 硬件加速引擎...")

    # 2. 开始微调训练！
    results = model.train(
        data="datasets/smoking_data/data.yaml",  # 指向刚才修改的教学大纲
        epochs=50,  # 训练 50 轮（M4 Pro 跑得快，50轮能出初步效果）
        imgsz=640,  # 输入尺寸
        batch=16,  # 每次喂 16 张图（利用你的大内存）
        device="mps",  # 🍎 核心密码：调用 Mac 专属的 MPS (Metal Performance Shaders) 加速！
        project="runs/train",  # 结果保存目录
        name="smoking_model_v1"  # 此次训练的名称
    )
    print("✅ 训练完成！权重已保存。")


if __name__ == '__main__':
    start_training()