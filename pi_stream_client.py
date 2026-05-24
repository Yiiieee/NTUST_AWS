import cv2
import socket
import time

"""Raspberry Pi video stream client

This client captures a local camera feed and streams JPEG frames to the PC host over TCP.
It reduces resolution and JPEG quality to improve network performance.
"""

PC_IP = '192.168.0.148'  # PC 的區域網路 IP
PC_PORT = 65434          # PC 接收影像的 Port

def get_camera():
    # 嘗試多個相機索引，因為在樹莓派上 /dev/video0 可能是硬體編解碼器，
    # 真正的 USB 攝影機（例如羅技相機）可能會在 /dev/video1 或 /dev/video2 等
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # 測試是否能成功讀取畫面
            ret, frame = cap.read()
            if ret:
                print(f"[+] 成功開啟相機，使用索引值: {i}")
                # 降低解析度以提升傳輸速度與流暢度
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                return cap
            else:
                cap.release()
    return None

def stream_video():
    cap = get_camera()

    if cap is None:
        print("無法開啟相機，請確認已連接")
        return

    while True:
        print(f"[*] 嘗試連線至 PC: {PC_IP}:{PC_PORT} 進行影像串流...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((PC_IP, PC_PORT))
                print(f"[+] 成功連線至 PC，開始傳送影像...")
                
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        print("無法讀取相機畫面，嘗試重新連接相機...")
                        cap.release()
                        time.sleep(2)
                        cap = get_camera()
                        if cap is None:
                            print("重新連接相機失敗，結束程式")
                            return
                        continue
                    
                    # 壓縮圖片為 JPEG 格式
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
                    result, encimg = cv2.imencode('.jpg', frame, encode_param)
                    if not result:
                        continue
                    
                    # 轉為 bytes 並傳送
                    data = encimg.tobytes()
                    client_socket.sendall(data)
                    
                    # 稍微延遲避免佔用過多網路頻寬
                    time.sleep(0.03)

        except ConnectionRefusedError:
            print(f"連線被拒絕。請確保 PC 端 ({PC_IP}) 已執行 pc_gesture.py 並且防火牆沒有阻擋。")
            time.sleep(3)
        except ConnectionResetError:
            print("PC 端已斷線，準備重新連線...")
            time.sleep(2)
        except Exception as e:
            print(f"串流中斷或發生錯誤: {e}")
            time.sleep(3)

    if cap is not None:
        cap.release()

if __name__ == '__main__':
    stream_video()