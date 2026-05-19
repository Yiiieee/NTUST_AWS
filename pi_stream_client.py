import cv2
import socket
import time

"""Raspberry Pi video stream client

This client captures a local camera feed and streams JPEG frames to the PC host over TCP.
It reduces resolution and JPEG quality to improve network performance.
"""

PC_IP = '192.168.0.148'  # PC 的區域網路 IP
PC_PORT = 65434          # PC 接收影像的 Port

def stream_video():
    # 開啟羅技相機
    cap = cv2.VideoCapture(0)
    
    # 降低解析度以提升傳輸速度與流暢度
    # 這樣做是為了讓網路串流更穩定，避免大量影像資料造成延遲。
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
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
                        print("無法讀取相機畫面")
                        break
                    
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
        except Exception as e:
            print(f"串流中斷或發生錯誤: {e}")
            time.sleep(3)

    cap.release()

if __name__ == '__main__':
    stream_video()