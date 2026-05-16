import cv2
import numpy as np
import mediapipe as mp
import socket
import time
import os
import glob
import threading
from deepface import DeepFace
from datetime import datetime
from cloud_sync import init_cloud_sync, upload_intruder

# ================= 參數設定 =================
PI_IP = '192.168.0.192'  # 樹莓派的 IP 地址
PI_PORT = 65432
PC_STREAM_PORT = 65434   # 接收影像串流的 Port

# 權限設定
OWNERS_DIR = "owners"           # 白名單照片的資料夾
INTRUDER_DIR = "intruders"      # 失敗照片的資料夾

# 建立相關資料夾
if not os.path.exists(OWNERS_DIR):
    os.makedirs(OWNERS_DIR)
if not os.path.exists(INTRUDER_DIR):
    os.makedirs(INTRUDER_DIR)

# ================= 影像接收執行緒 =================
latest_frame_data = b''
stream_active = False

def receive_tcp_stream():
    """背景執行緒：負責接收樹莓派傳來的即時影像 TCP 串流"""
    global latest_frame_data, stream_active
    HOST = '0.0.0.0'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PC_STREAM_PORT))
        server_socket.listen()
        print(f"[*] 等待樹莓派影像串流連線 (TCP Port {PC_STREAM_PORT})...")
        
        while True:
            try:
                conn, addr = server_socket.accept()
                stream_active = True
                print(f"[+] 樹莓派已連線，開始接收即時影像: {addr}")
                buffer = b''
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    buffer += data
                    
                    # 尋找 JPEG 圖片的開頭 (FF D8) 與結尾 (FF D9)
                    a = buffer.find(b'\xff\xd8')
                    b = buffer.find(b'\xff\xd9')
                    
                    if a != -1 and b != -1 and b > a:
                        latest_frame_data = buffer[a:b+2]
                        buffer = buffer[b+2:]
            except Exception as e:
                print(f"連線中斷: {e}")
            finally:
                stream_active = False
                if 'conn' in locals():
                    conn.close()
                print("樹莓派影像已斷線，等待重新連線...")

# ================= 建立連線 =================
def connect_to_pi():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((PI_IP, PI_PORT))
        print(f" 成功連線至樹莓派 {PI_IP}:{PI_PORT} (馬達控制)")
        return s
    except Exception as e:
        print(f" 無法連線到樹莓派: {e}")
        return None

# ================= 手勢辨識設定 =================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# ================= 人臉偵測設定 =================
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(
    model_selection=0, 
    min_detection_confidence=0.6
)

def count_fingers(hand_landmarks):
    """ 簡單計算伸出的手指數量 """
    finger_tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    finger_pips = [
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP
    ]
    
    count = 0
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            count += 1
            
    idx_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x
    
    if idx_mcp < pinky_mcp:
        if thumb_tip < thumb_ip:
            count += 1
    else:
        if thumb_tip > thumb_ip:
            count += 1
            
    return count

def is_blurry(image, threshold=80.0):
    """ 計算影像的拉普拉斯變異數，數值越低代表越模糊 """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance < threshold, variance

def apply_clahe(image):
    """ 應用 CLAHE (限制對比度自適應直方圖均衡化) 以對抗背光和昏暗環境 """
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

def main():
    owner_images = glob.glob(os.path.join(OWNERS_DIR, "*.[jJ][pP][gG]")) + glob.glob(os.path.join(OWNERS_DIR, "*.[pP][nN][gG]"))
    if not owner_images:
        print(f"找不到照片！請先放至少一張照片到 {OWNERS_DIR} 資料夾中。")
    else:
        print(f"已在 {OWNERS_DIR} 資料夾中找到 {len(owner_images)} 照片。")

    print("\n========== 初始化 (Supabase) ==========")
    init_cloud_sync()

    # 連線到樹莓派 (發送馬達指令用)
    pi_socket = connect_to_pi()
    
    # 啟動背景執行緒接收樹莓派影像
    t = threading.Thread(target=receive_tcp_stream, daemon=True)
    t.start()
    
    # 開啟本機相機作為備用 (如果樹莓派沒開相機，就先用筆電相機)
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("已開啟本機攝影機 0 (當樹莓派未連線時備用)")

    try:
        last_signal_time = 0
        COOLDOWN = 10.0  
        
        print("開始讀取影像與手勢辨識...")
        while True:
            success = False
            img = None
            
            # 優先使用樹莓派傳來的即時影像
            if stream_active and latest_frame_data:
                np_arr = np.frombuffer(latest_frame_data, np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                if img is not None:
                    success = True
                    
            # 如果樹莓派沒畫面，回退到筆電本身的相機
            if not success:
                success, img = cap.read()
                if not success:
                    print("無法讀取畫面，重試中...")
                    time.sleep(1)
                    continue

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ih, iw, _ = img.shape
            
            # --- 繪製固定導引框 ---
            # 讓使用者把臉對準這個框，徹底排除背景干擾
            box_size = 300
            box_x1 = max(0, (iw - box_size) // 2)
            box_y1 = max(0, (ih - box_size) // 2)
            box_x2 = min(iw, box_x1 + box_size)
            box_y2 = min(ih, box_y1 + box_size)
            
            cv2.rectangle(img, (box_x1, box_y1), (box_x2, box_y2), (0, 255, 0), 2)
            cv2.putText(img, "Put Face Here", (box_x1, box_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # 擷取框內的影像作為唯一的辨識來源
            target_crop = img[box_y1:box_y2, box_x1:box_x2]
            
            results = hands.process(img_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    fingers = count_fingers(hand_landmarks)
                    cv2.putText(img, f"Fingers: {fingers}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    current_time = time.time()
                    if fingers == 1 and (current_time - last_signal_time > COOLDOWN):
                        print("=====================================")
                        print(" 偵測到手勢 '1'，開始進行人臉身分驗證...")
                        
                        if target_crop is None or target_crop.size == 0:
                            print(" 畫面異常，請重試！")
                            last_signal_time = current_time
                            continue
                            
                        # 檢查影像是否過於模糊 (只檢查目標框內)
                        blurry, var = is_blurry(target_crop, threshold=50.0) # 稍微放寬防模糊標準
                        if blurry:
                            print(f" 警告：影像過於模糊 (清晰度: {var:.2f})，請保持靜止！")
                            cv2.putText(img, f"BLURRY: {var:.1f} - STAY STILL!", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                            continue
                            
                        # 應用 CLAHE 影像強化 (只針對目標框，杜絕背景干擾)
                        enhanced_crop = apply_clahe(target_crop)
                        print(f" (已套用 CLAHE 影像強化，清晰度: {var:.2f})")
                        
                        owner_images = glob.glob(os.path.join(OWNERS_DIR, "*.[jJ][pP][gG]")) + glob.glob(os.path.join(OWNERS_DIR, "*.[pP][nN][gG]"))
                        
                        if not owner_images:
                            print(f" 錯誤：{OWNERS_DIR} 資料夾中沒有任何照片，拒絕進入！")
                            last_signal_time = current_time
                            continue
                        
                        is_verified = False
                        matched_owner = ""
                        
                        try:
                            print(f" 正在與第{len(owner_images)}張照片進行比對，請稍候...")
                            
                            for owner_img_path in owner_images:
                                owner_img = cv2.imdecode(np.fromfile(owner_img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
                                
                                if owner_img is None:
                                    continue
                                    
                                try:
                                    # 1. 第一關：ArcFace 驗證 (只傳入無背景的 enhanced_crop)
                                    match_result = DeepFace.verify(
                                        img1_path=owner_img,            
                                        img2_path=enhanced_crop,           
                                        model_name="ArcFace",         
                                        detector_backend="opencv", # 框內已經是乾淨的臉，用 opencv 即可
                                        enforce_detection=True
                                    )
                                    
                                    distance = match_result.get("distance", 1.0)
                                    deepface_verified = match_result.get("verified", False)
                                    print(f"   -> [ArcFace] {os.path.basename(owner_img_path)} | 距離: {distance:.4f} | 判定: {deepface_verified}")
                                    
                                    # 極高置信度通過
                                    if deepface_verified and distance < 0.45:
                                        is_verified = True
                                        matched_owner = os.path.basename(owner_img_path)
                                        # 自動學習機制：如果是極度清晰且非常確定的本人，存起來當作未來參考
                                        if distance < 0.25 and len(owner_images) < 15:
                                            new_path = os.path.join(OWNERS_DIR, f"auto_learn_{int(time.time())}.jpg")
                                            cv2.imwrite(new_path, img)
                                            print(f"   ★ [自動學習] 已儲存高置信度臉部特徵至白名單！")
                                        break
                                        
                                    # 2. 第二關 (Fallback)：如果 ArcFace 些微差距沒過，啟動 Facenet 雙重驗證
                                    elif distance < 0.60:
                                        print(f"   -> ArcFace 些微差距未過，啟用 Facenet 二次確認...")
                                        fallback_result = DeepFace.verify(
                                            img1_path=owner_img,            
                                            img2_path=enhanced_crop,           
                                            model_name="Facenet",         
                                            detector_backend="opencv",     
                                            enforce_detection=True
                                        )
                                        f_distance = fallback_result.get("distance", 1.0)
                                        f_verified = fallback_result.get("verified", False)
                                        print(f"   -> [Facenet] {os.path.basename(owner_img_path)} | 距離: {f_distance:.4f} | 判定: {f_verified}")
                                        
                                        # Facenet 預設門檻大約是 0.40
                                        if f_verified and f_distance < 0.35:
                                            print("   ★ [雙模型驗證] Facenet 確認為本人！")
                                            is_verified = True
                                            matched_owner = os.path.basename(owner_img_path)
                                            break

                                except Exception as ve:
                                    print(f" 警告：比對 {os.path.basename(owner_img_path)} 時發生錯誤。({ve})")
                                    continue
                            
                            if is_verified:
                                print(f" 驗證成功！符合的身分: {matched_owner}")
                                print(" 準備發送開門訊號至樹莓派！")
                                cv2.putText(img, "ACCESS GRANTED", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                                
                                if pi_socket:
                                    try:
                                        pi_socket.sendall(b"1")
                                        pi_socket.setblocking(False)
                                        try:
                                            resp = pi_socket.recv(1024)
                                            print(f" 樹莓派回傳: {resp.decode().strip()}")
                                        except BlockingIOError:
                                            pass
                                        pi_socket.setblocking(True)
                                    except Exception as e:
                                        print(f" 傳送失敗，嘗試重新連線... 錯誤: {e}")
                                        pi_socket = connect_to_pi()
                            else:
                                print(" 驗證失敗！拒絕進入。")
                                cv2.putText(img, "ACCESS DENIED", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                                
                                if pi_socket:
                                    try:
                                        pi_socket.sendall(b"0")
                                        pi_socket.setblocking(False)
                                        try:
                                            resp = pi_socket.recv(1024)
                                            print(f" 樹莓派回傳: {resp.decode().strip()}")
                                        except BlockingIOError:
                                            pass
                                        pi_socket.setblocking(True)
                                    except Exception as e:
                                        print(f" 傳送 '0' 失敗，嘗試重新連線... 錯誤: {e}")
                                        pi_socket = connect_to_pi()
                                
                                timestamp = time.strftime("%Y%m%d_%H%M%S")
                                intruder_filename = os.path.join(INTRUDER_DIR, f"intruder_{timestamp}.jpg")
                                cv2.imwrite(intruder_filename, img)
                                print(f" 已拍下闖入者照片並存至: {intruder_filename}")
                                
                                _, img_encoded = cv2.imencode('.jpg', img)
                                upload_intruder(image_path=intruder_filename, image_bytes=img_encoded.tobytes())
                                
                        except Exception as e:
                            print(f" 人臉辨識發生錯誤: {e}")
                            
                        last_signal_time = time.time()  
                        
                        for _ in range(5):
                            if stream_active:
                                time.sleep(0.1)
                            else:
                                cap.read()

            # 顯示來源提示
            source_txt = "Source: Raspberry Pi" if stream_active else "Source: Local WebCam"
            cv2.putText(img, source_txt, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            cv2.imshow("PC Gesture & Face Control", img)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                print("收到離開指令，準備關閉...")
                break
                
    except KeyboardInterrupt:
        print("\n使用者強制中斷程式 (Ctrl+C)")
    except Exception as e:
        print(f"\n程式發生非預期錯誤: {e}")
    finally:
        print("\n========== 正在釋放相機與連線資源 ==========")
        if 'cap' in locals() and cap is not None and cap.isOpened():
            cap.release()
            print("✓ 相機資源已釋放")
        cv2.destroyAllWindows()
        print("✓ 顯示視窗已關閉")
        if 'pi_socket' in locals() and pi_socket:
            pi_socket.close()
            print("✓ 樹莓派連線已關閉")
        print("程式結束。")

if __name__ == '__main__':
    main()
