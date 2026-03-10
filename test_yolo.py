from ultralytics import YOLO

# 加载模型
model = YOLO("yolov8n.pt")

# 测试预测
results = model.predict(source="https://ultralytics.com/images/bus.jpg", show=True)
print("检测完成！看看弹出的窗口吧。")