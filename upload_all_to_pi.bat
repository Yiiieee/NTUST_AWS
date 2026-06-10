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
echo 正在上傳程式檔案 (將會提示輸入樹莓派的密碼)...
cd /d "%~dp0"
scp pi_motor_server.py test_motor.py pi_stream_client.py %PI_USER%@%PI_IP%:%TARGET_DIR%

echo.
echo ==========================================
echo 傳輸完成！按任意鍵關閉此視窗
echo ==========================================
pause