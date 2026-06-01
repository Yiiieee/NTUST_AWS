@echo off
chcp 65001 >nul

:: 在這裡設定你的樹莓派 IP 和帳號
set PI_IP=172.20.10.2
set PI_USER=ziv
set TARGET_DIR=/home/ziv/workspace/

echo ==========================================
echo 準備上傳最新程式到樹莓派
echo 目標 IP: %PI_IP%
echo ==========================================
echo.
echo [1/3] 上傳馬達伺服器 (pi_motor_server.py)...
scp "c:\Users\h0928\OneDrive\桌面\VScode\AWS\pi_motor_server.py" %PI_USER%@%PI_IP%:%TARGET_DIR%

echo [2/3] 上傳馬達測試腳本 (test_motor.py)...
scp "c:\Users\h0928\OneDrive\桌面\VScode\AWS\test_motor.py" %PI_USER%@%PI_IP%:%TARGET_DIR%

echo [3/3] 上傳影像串流客戶端 (pi_stream_client.py)...
scp "c:\Users\h0928\OneDrive\桌面\VScode\AWS\pi_stream_client.py" %PI_USER%@%PI_IP%:%TARGET_DIR%

echo.
echo ==========================================
echo 傳輸完成！按任意鍵關閉此視窗
echo ==========================================
pause