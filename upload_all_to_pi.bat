@echo off
chcp 65001 >nul
echo ==========================================
echo 準備上傳最新程式到樹莓派
echo 目標 IP: 192.168.0.192
echo ==========================================
echo.

echo [1/3] 正在上傳馬達控制伺服器 (pi_motor_server.py)...
scp "c:\Users\h0928\OneDrive\桌面\VScode\AWS\pi_motor_server.py" ziv@192.168.0.192:/home/ziv/workspace/

echo [2/3] 正在上傳影像串流程式 (pi_stream_client.py)...
scp "c:\Users\h0928\OneDrive\桌面\VScode\AWS\pi_stream_client.py" ziv@192.168.0.192:/home/ziv/workspace/

echo [3/3] 正在上傳網頁相機程式 (pi_camera_web.py)...
scp "c:\Users\h0928\OneDrive\桌面\VScode\AWS\pi_camera_web.py" ziv@192.168.0.192:/home/ziv/workspace/

echo.
echo ==========================================
echo 傳輸完成！你可以按任意鍵關閉此視窗。
echo ==========================================
pause