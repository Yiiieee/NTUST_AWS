import cv2
import numpy as np
import mediapipe as mp
import socket
import time
import os
import glob
from deepface import DeepFace

# ================= 參數設定 =================
PI_IP = '192.168.x.x'  # 樹莓派的 IP 地址
PI_PORT = 65432

# tcp 串流
STREAM_URL = 'http://192.168.x.x:8080/?action=stream' #  影像網址

# 權限設定
OWNERS_DIR = "owners"           # 白名單照片的資料夾
INTRUDER_DIR = "intruders"      # 失敗照片的資料夾

# 建立相關資料夾
if not os.path.exists(OWNERS_DIR):
    os.makedirs(OWNERS_DIR)
if not os.path.exists(INTRUDER_DIR):
    os.makedirs(INTRUDER_DIR)

# ================= 建立連線 =================
def connect_to_pi():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((PI_IP, PI_PORT))
        print(f" 成功連線至樹莓派 {PI_IP}:{PI_PORT}")
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
    # 1. 判斷四指 
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            count += 1
            
    # 2. 判斷大拇指 
    idx_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x
    
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x
    
    # 手心/手背
    if idx_mcp < pinky_mcp:
     
        if thumb_tip < thumb_ip:
            count += 1
    else:
        
        if thumb_tip > thumb_ip:
            count += 1
            
    return count

def main():
    
    owner_images = glob.glob(os.path.join(OWNERS_DIR, "*.[jJ][pP][gG]")) + glob.glob(os.path.join(OWNERS_DIR, "*.[pP][nN][gG]"))
    if not owner_images:
        print(f"找不到照片！請先放至少一張照片到 {OWNERS_DIR} 資料夾中。")
    else:
        print(f"已在 {OWNERS_DIR} 資料夾中找到 {len(owner_images)} 照片。")

    # 連線到樹莓派
    pi_socket = connect_to_pi()
    
    # 開啟影像串流 
    cap = cv2.VideoCapture(STREAM_URL)
    
    if not cap.isOpened():
        print(f"無法開啟影像串流: {STREAM_URL}")
        print("切換回本機測試鏡頭 (0)")
        cap = cv2.VideoCapture(0)

    last_signal_time = 0
    COOLDOWN = 5.0  # 偵測的冷卻時間 

    print("開始讀取影像與手勢辨識...")
    while True:
        success, img = cap.read()
        if not success:
            print("無法讀取畫面，重試中...")
            time.sleep(1)
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        face_crop = None
        face_results = face_detection.process(img_rgb)
        if face_results.detections:
            # 取出第一個偵測到的人臉
            detection = face_results.detections[0]
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = img.shape
            x = int(bboxC.xmin * iw)
            y = int(bboxC.ymin * ih)
            w = int(bboxC.width * iw)
            h = int(bboxC.height * ih)
            
            #  margin 
            margin_x = int(w * 0.2)
            margin_y = int(h * 0.2)
            x1 = max(0, x - margin_x)
            y1 = max(0, y - margin_y)
            x2 = min(iw, x + w + margin_x)
            y2 = min(ih, y + h + margin_y)
            
            # 畫出 Box line 
            # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
            # cv2.putText(img, "Face Align", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            face_crop = img[y1:y2, x1:x2]
        
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                fingers = count_fingers(hand_landmarks)
                cv2.putText(img, f"Fingers: {fingers}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                current_time = time.time()
                # 當偵測到手勢 1，且過了冷卻時間
                if fingers == 1 and (current_time - last_signal_time > COOLDOWN):
                    print("=====================================")
                    print(" 偵測到手勢 '1'，開始進行人臉身分驗證...")
                    
                    # Box line裁切後再送給 DeepFace
                    face_crop = None
                    with mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6) as recognition_face_detection:
                        recognition_results = recognition_face_detection.process(img_rgb)
                        if recognition_results.detections:
                            # 取出第一個偵測到的人臉
                            detection = recognition_results.detections[0]
                            bboxC = detection.location_data.relative_bounding_box
                            ih, iw, _ = img.shape
                            x = int(bboxC.xmin * iw)
                            y = int(bboxC.ymin * ih)
                            w = int(bboxC.width * iw)
                            h = int(bboxC.height * ih)
                            
                            # 加上 margin 確保完整包含臉部
                            margin_x = int(w * 0.2)
                            margin_y = int(h * 0.2)
                            x1 = max(0, x - margin_x)
                            y1 = max(0, y - margin_y)
                            x2 = min(iw, x + w + margin_x)
                            y2 = min(ih, y + h + margin_y)
                            
                            #  照片上的 Box line 
                            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
                            cv2.putText(img, "Face Crop", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                            
                            face_crop = img[y1:y2, x1:x2]
                    
                    if face_crop is None or face_crop.size == 0:
                        print(" 畫面中未偵測到清晰的人臉，請重試！")
                        cv2.putText(img, "NO FACE DETECTED", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)
                        last_signal_time = current_time
                        continue
                    
                    # 重新讀取照片清單
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
                                print(f"  無法讀取照片: {owner_img_path}")
                                continue
                                
                            match_result = DeepFace.verify(
                                img1_path=owner_img,            
                                img2_path=face_crop,           
                                model_name="ArcFace",         
                                detector_backend="opencv",     
                                enforce_detection=False
                            )
                            
                            if match_result["verified"]:
                                is_verified = True
                                matched_owner = os.path.basename(owner_img_path)
                                break 
                        
                        if is_verified:
                            print(f" 驗證成功！符合的身分: {matched_owner}")
                            print(" 準備發送開門訊號至樹莓派！")
                            cv2.putText(img, "ACCESS GRANTED", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                            
                            # 發送訊號
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
                            print(" 驗證失敗！拒絕進入。所有白名單皆不符合。")
                            cv2.putText(img, "ACCESS DENIED", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                            
                            # 儲存闖入者照片
                            timestamp = time.strftime("%Y%m%d_%H%M%S")
                            intruder_filename = os.path.join(INTRUDER_DIR, f"intruder_{timestamp}.jpg")
                            cv2.imwrite(intruder_filename, img)
                            print(f" 已拍下闖入者照片並存至: {intruder_filename}")
                            
                    except Exception as e:
                        print(f" 人臉辨識發生錯誤: {e}")
                        
                    last_signal_time = time.time()  # 更新時間避免連續觸發

        # 顯示影像
        cv2.imshow("PC Gesture & Face Control", img)
        
        # 按 'q' 離開
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    cap.release()
    cv2.destroyAllWindows()
    if pi_socket:
        pi_socket.close()

if __name__ == '__main__':
    main()
