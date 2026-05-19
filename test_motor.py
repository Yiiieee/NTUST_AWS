import time
import sys

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("錯誤：無法載入 RPi.GPIO 模組。請確認您正在樹莓派上執行，或已安裝該模組。")
    sys.exit(1)

# ================= 參數設定 =================
MOTOR_PINS = [17, 18, 27, 22]  # ULN2003 接到的 GPIO (BCM 模式)
STEP_DELAY = 0.005             # 增加每步停頓時間 (秒) - 放慢速度以確認是否因為速度過快導致馬達失步
STEP_COUNT = 512               # 測試轉動步數 (512步大約是一圈)

# 28BYJ-48 半步階序 (8 steps)
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

def setup():
    print("初始化 GPIO 腳位...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in MOTOR_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

def cleanup():
    print("清理 GPIO 腳位並關閉馬達電源...")
    for pin in MOTOR_PINS:
        GPIO.output(pin, 0)
    GPIO.cleanup()

def test_wiring():
    print("====================================")
    print("開始線路測試模式（請看驅動板上的 LED）")
    print("燈號應該要『依序』單獨亮起：IN1 -> IN2 -> IN3 -> IN4")
    print("如果跳著亮（例如 1 -> 3 -> 2 -> 4），代表您的杜邦線接錯順序了！")
    print("====================================")
    
    for i, pin in enumerate(MOTOR_PINS):
        print(f"正在點亮 IN{i+1} (對應 GPIO {pin})...")
        GPIO.output(pin, 1)
        time.sleep(1.5)  # 亮 1.5 秒讓使用者看清楚
        GPIO.output(pin, 0)
        time.sleep(0.5)
    print("線路測試結束。\n")

def step_motor(steps, direction=1):
    sequence = STEP_SEQUENCE if direction == 1 else list(reversed(STEP_SEQUENCE))
    count = len(sequence)

    for step in range(steps):
        seq_index = step % count
        pattern = sequence[seq_index]
        for pin, value in zip(MOTOR_PINS, pattern):
            GPIO.output(pin, value)
        time.sleep(STEP_DELAY)

def test():
    try:
        setup()
        
        # 先執行線路測試
        test_wiring()
        
        print(f"測試：正轉 {STEP_COUNT} 步...")
        step_motor(STEP_COUNT, direction=1)
        time.sleep(1)
        
        print(f"測試：反轉 {STEP_COUNT} 步...")
        step_motor(STEP_COUNT, direction=-1)
        time.sleep(1)
        
        print("測試完成！")
        
    except KeyboardInterrupt:
        print("\n使用者強制中斷測試。")
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        cleanup()

if __name__ == '__main__':
    test()
