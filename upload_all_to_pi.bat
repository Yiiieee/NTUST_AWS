@echo off
chcp 65001 >nul
echo ==========================================
echo 準備上傳最新程式到樹莓派
echo 目標 IP: 192.168.0.192
echo ==========================================
echo.
echo [1/3] 上傳馬達伺服器 (pi_motor_server.py)...
scp "c:\Users\h0928\OneDrive\桌面\VScode\AWS\pi_motor_server.py" ziv@192.168.0.192:/home/ziv/workspace/

echo [2/3] 上傳馬達測試腳本 (test_motor.py)...
scp "c:\Users\h0928\OneDrive\桌面\VScode\AWS\test_motor.py" ziv@192.168.0.192:/home/ziv/workspace/

echo [3/3] 上傳影像串流客戶端 (pi_stream_client.py)...
scp "c:\Users\h0928\OneDrive\桌面\VScode\AWS\pi_stream_client.py" ziv@192.168.0.192:/home/ziv/workspace/

echo.
echo ==========================================
echo 傳輸完成！按任意鍵關閉此視窗
echo ==========================================
pause