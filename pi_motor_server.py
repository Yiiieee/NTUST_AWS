import socket
import time
import RPi.GPIO as GPIO

# ================= 參數設定 =================
HOST = '0.0.0.0'  # 監聽所有網路介面
PORT = 65432      # 監聽的 Port

#  GPIO 腳位 (BCM 編號)
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# 步進馬達的控制序列 
STEP_SEQUENCE = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
motor_pins = [IN1, IN2, IN3, IN4]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

def motor_step(steps, delay=0.001):
    """控制馬達轉動指定的步數"""
    print(f"馬達開始轉動: {steps} 步")
    step_count = len(STEP_SEQUENCE)
    direction = 1 if steps > 0 else -1
    steps = abs(steps)
    
    for i in range(steps):
        seq = STEP_SEQUENCE[(i * direction) % step_count]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)
        time.sleep(delay)
        
    # 轉完後將所有腳位設為 0 以避免發熱
    for pin in motor_pins:
        GPIO.output(pin, 0)
    print("馬達轉動結束")

def start_server():
    """啟動 Socket 伺服器監聽 PC 指令"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 設定 SO_REUSEADDR 避免重啟時遇到 Address already in use
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] 樹莓派伺服器啟動，監聽 {HOST}:{PORT}")
        
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print(f"[+] 來自 {addr} 的連線")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        
                        cmd = data.decode('utf-8').strip()
                        print(f"收到指令: {cmd}")
                        
                        if cmd == '1':
                           
                            motor_step(512) # 約90度
                            conn.sendall(b"Motor Activated\n")
            except Exception as e:
                print(f"發生錯誤: {e}")
            except KeyboardInterrupt:
                print("\n伺服器關閉")
                break

if __name__ == '__main__':
    try:
        start_server()
    finally:
        GPIO.cleanup()
