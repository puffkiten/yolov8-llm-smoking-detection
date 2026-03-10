import cv2
from ultralytics import YOLO


def test_webcam_robust():
    # 1. 加载模型 (请确保路径还是你刚才那个正确的路径)
    model_path = "runs/detect/runs/train/smoking_model_v1/weights/best.pt"
    model = YOLO(model_path)

    # 2. 手动接管摄像头控制权！
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ 无法打开摄像头！")
        return

    print("📷 摄像头已成功接管！画面即将弹出...")
    print("💡 在弹出的视频窗口上，按键盘的 'q' 键安全退出。")

    # 3. 开启死循环，一帧一帧地处理 (这就是未来后端处理视频流的核心逻辑)
    while True:
        success, frame = cap.read()  # 抓取一帧画面
        if not success:
            print("❌ 画面读取失败！")
            break

        # 4. 把这一帧喂给 AI 找香烟 (verbose=False 可以让终端不再疯狂刷屏)
        results = model(frame, conf=0.7, verbose=False)

        # 5. 让 YOLO 把找到的框，画在我们的画面上
        annotated_frame = results[0].plot()

        # 6. 强制弹窗并置顶显示
        cv2.imshow("Mac M4 Pro - Smoking Detection AI", annotated_frame)

        # 7. 监听键盘，如果按下 'q' 就打破循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 收到退出指令，正在关闭摄像头...")
            break

    # 8. 优雅地打扫战场（关掉摄像头绿灯，销毁所有窗口）
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    test_webcam_robust()