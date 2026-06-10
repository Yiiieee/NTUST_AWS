import time
import sys

try:
    from gpiozero import LED
except ImportError:
    print("錯誤：無法載入 gpiozero 模組。請確認您正在樹莓派上執行，或已安裝該模組 (pip install gpiozero)。")
    sys.exit(1)

# ================= 參數設定 =================
# ULN2003 接到的 GPIO (BCM 模式)
MOTOR_PINS = [17, 18, 27, 22] 
# 使用 gpiozero 的 LED 類別來控制輸出引腳
try:
    motor_pins = [LED(pin) for pin in MOTOR_PINS]
except Exception as e:
    print(f"初始化 GPIO 失敗: {e}")
    print("請確認沒有其他程式正在使用這些腳位，或者嘗試重開機。")
    sys.exit(1)

# 減少每步停頓時間 (秒) 以加快速度
# 注意：28BYJ-48 的極限大約在 0.001 左右，太快會導致馬達空轉(失步)且發出怪聲
STEP_DELAY = 0.0015             
# 28BYJ-48 步進馬達內部轉子轉一圈是 64 步，加上減速比 1:64，所以外部軸轉一圈需要 64 * 64 = 4096 步 (半步模式)
# 360度 = 4096步，90度 = 4096 / 4 = 1024 步
#STEP_COUNT_90_DEG = 1200
STEP_COUNT_90_DEG = 8192

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

def stop_motor():
    """切斷所有線圈的電流，防止馬達持續發熱"""
    for pin in motor_pins:
        pin.off()

def cleanup():
    print("清理 GPIO 腳位並關閉馬達電源...")
    stop_motor()

def step_motor(steps, direction=1):
    sequence = STEP_SEQUENCE if direction == 1 else list(reversed(STEP_SEQUENCE))
    count = len(sequence)

    for step in range(steps):
        seq_index = step % count
        pattern = sequence[seq_index]
        for pin, value in zip(motor_pins, pattern):
            if value:
                pin.on()
            else:
                pin.off()
        time.sleep(STEP_DELAY)

def test():
    try:
        print(f"測試開始：正轉 90 度 ({STEP_COUNT_90_DEG} 步)...")
        step_motor(STEP_COUNT_90_DEG, direction=1)
        stop_motor() # 轉完後立即斷電防燙

        print("等待 1 秒...")
        time.sleep(1)

        print(f"測試開始：反轉 90 度 ({STEP_COUNT_90_DEG} 步)...")
        step_motor(STEP_COUNT_90_DEG, direction=-1)
        stop_motor() # 轉完後立即斷電防燙

        print("測試完成！")

    except KeyboardInterrupt:
        print("\n使用者強制中斷測試。")
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        cleanup()

if __name__ == '__main__':
    test()
