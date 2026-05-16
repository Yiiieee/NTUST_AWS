import socket
import time

# ================= 參數設定 =================
HOST = '0.0.0.0'  # 監聽所有網路介面
PORT = 65432      # 監聽的 Port

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
                            print("====================")
                            print("     收到指令1      ")
                            print("====================")
                            conn.sendall(b"Motor Activated\n")
            except Exception as e:
                print(f"發生錯誤: {e}")
            except KeyboardInterrupt:
                print("\n伺服器關閉")
                break

if __name__ == '__main__':
    start_server()