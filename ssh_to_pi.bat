@echo off
chcp 65001 >nul
py "%~dp0ssh_to_pi.py" %* || python "%~dp0ssh_to_pi.py" %*
