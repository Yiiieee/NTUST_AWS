import winreg
import os
import sys

def check_camera_usage():
    print("正在檢查相機占用狀態 (Windows 10/11)...\n")
    
    # Windows 隱私權設定中，紀錄應用程式存取硬體的登錄檔路徑
    base_key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"
    
    try:
        base_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_key_path)
    except Exception as e:
        print("無法存取登錄檔，可能您的 Windows 版本不支援此檢查方式。")
        return

    in_use_by = []
    
    # 1. 檢查 UWP 應用程式 (Microsoft Store apps，例如 Windows 內建的「相機」App)
    try:
        num_subkeys, _, _ = winreg.QueryInfoKey(base_key)
        for i in range(num_subkeys):
            app_name = winreg.EnumKey(base_key, i)
            if app_name == "NonPackaged":
                continue
            
            try:
                app_key = winreg.OpenKey(base_key, app_name)
                stop_time, _ = winreg.QueryValueEx(app_key, "LastUsedTimeStop")
                # 如果 LastUsedTimeStop 是 0，代表程式「正在」使用相機
                if stop_time == 0:
                    in_use_by.append(f"[UWP App] {app_name}")
                winreg.CloseKey(app_key)
            except FileNotFoundError:
                pass
    except Exception as e:
        pass

    # 2. 檢查傳統桌面應用程式 (NonPackaged，例如 OBS, Zoom, Python, Chrome 等)
    try:
        non_packaged_key = winreg.OpenKey(base_key, "NonPackaged")
        num_subkeys, _, _ = winreg.QueryInfoKey(non_packaged_key)
        for i in range(num_subkeys):
            exe_path = winreg.EnumKey(non_packaged_key, i)
            try:
                app_key = winreg.OpenKey(non_packaged_key, exe_path)
                stop_time, _ = winreg.QueryValueEx(app_key, "LastUsedTimeStop")
                if stop_time == 0:
                    # 登錄檔會把路徑的 '\' 替換成 '#'，我們把它換回來以便閱讀
                    actual_path = exe_path.replace("#", "\\")
                    in_use_by.append(f"[桌面程式] {actual_path}")
                winreg.CloseKey(app_key)
            except FileNotFoundError:
                pass
        winreg.CloseKey(non_packaged_key)
    except FileNotFoundError:
        pass
        
    winreg.CloseKey(base_key)
    
    # 輸出結果
    if in_use_by:
        print("[警告] 偵測到以下程式目前可能正在使用您的相機：")
        for app in in_use_by:
            print(f"  -> {app}")
        print("\n請關閉上述程式後，再重新執行 pc_gesture.py。")
    else:
        print("[正常] 系統紀錄顯示，目前沒有任何程式正在使用相機。")
        print("\n（如果相機依然無法開啟，可能是 USB 驅動卡死，建議：")
        print(" 1. 重新插拔您的外接攝影機。")
        print(" 2. 在裝置管理員中停用再啟用相機。")
        print(" 3. 重新開機。）")

if __name__ == "__main__":
    check_camera_usage()
