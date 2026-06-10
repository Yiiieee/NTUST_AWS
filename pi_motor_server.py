import socket
import time

try:
    import RPi.GPIO as GPIO # type: ignore
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

"""Raspberry Pi motor server

This server listens for commands from the PC and drives a stepper motor via GPIO.
Command '1' activates the motor, and '0' is treated as no-action.
"""

# ================= 參數設定 =================
HOST = '0.0.0.0'  # 監聽所有網路介面
PORT = 65432      # 監聽的 Port
MOTOR_PINS = [17, 18, 27, 22]  # ULN2003 接到的 GPIO
STEP_DELAY = 0.0015  # 每步停頓時間 (秒)
STEP_COUNT_90_DEG = 8192  # 轉動步數 (90度)

# 28BYJ-48 半步階序
STEP_SEQUENCE = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]


def setup_gpio():
    # GPIO 初始化，確保馬達驅動腳位已設定為輸出並預設為低電位
    if not GPIO_AVAILABLE:
        print("警告：RPi.GPIO 模組無法載入，無法驅動馬達。請在樹莓派上安裝或確認環境。")
        return

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in MOTOR_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)


def cleanup_gpio():
    if GPIO_AVAILABLE:
        for pin in MOTOR_PINS:
            GPIO.output(pin, 0)
        GPIO.cleanup()


def step_motor(steps, direction=1):
    if not GPIO_AVAILABLE:
        return

    sequence = STEP_SEQUENCE if direction == 1 else list(reversed(STEP_SEQUENCE))
    count = len(sequence)

    for step in range(steps):
        seq_index = step % count
        pattern = sequence[seq_index]
        for pin, value in zip(MOTOR_PINS, pattern):
            GPIO.output(pin, value)
        time.sleep(STEP_DELAY)

    for pin in MOTOR_PINS:
        GPIO.output(pin, 0)


def activate_motor():
    if not GPIO_AVAILABLE:
        print("無法驅動馬達，RPi.GPIO 不可用。")
        return

    print("====================")
    print("     開始驅動馬達      ")
    print("====================")
    
    print(f"正在開門({STEP_COUNT_90_DEG} 步)...")
    step_motor(STEP_COUNT_90_DEG, direction=1)
    
    print("等待 1 秒...")
    time.sleep(1)
    
    print(f"正在關門({STEP_COUNT_90_DEG} 步)...")
    step_motor(STEP_COUNT_90_DEG, direction=-1)
    
    print("馬達轉動完成。")


def start_server():
    """啟動 Socket 伺服器監聽 PC 指令

    這個伺服器會一直等待 PC 端連線，接收字串指令並觸發馬達運作。
    """
    setup_gpio()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 設定 SO_REUSEADDR 避免重啟時遇到 Address already in use
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] 樹莓派伺服器啟動，監聽 {HOST}:{PORT}")

        try:
            while True:
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
                            print("收到指令 1：啟動馬達")
                            activate_motor()
                            conn.sendall(b"Motor Activated\n")
                        elif cmd == '0':
                            print("收到指令 0：不驅動馬達")
                            conn.sendall(b"Motor Skipped\n")
                        else:
                            print(f"未知指令：{cmd}")
                            conn.sendall(b"Unknown Command\n")
        except KeyboardInterrupt:
            print("\n伺服器關閉")
        except Exception as e:
            print(f"發生錯誤: {e}")
        finally:
            cleanup_gpio()


if __name__ == '__main__':
    start_server()
