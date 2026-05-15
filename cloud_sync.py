import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
import cv2
import base64
from supabase import create_client, Client
import threading
import time

# ================= Supabase 設定 =================
SUPABASE_URL = "https://iyzkimsbcvzxzhbvvlrf.supabase.co"
SUPABASE_KEY = "sb_publishable_9UyTV4wxUCkC2jwqTpSsoQ_91b64QoX"

# 本地暫存設定
CACHE_DB = "cloud_sync_cache.db"
SYNC_QUEUE = "sync_queue.json"

class CloudSync:
    def __init__(self):
        """初始化雲端同步模組"""
        try:
            self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            self.connected = True
            print("✓ 成功連線至 Supabase")
        except Exception as e:
            self.connected = False
            print(f"✗ Supabase 連線失敗: {e}")
        
        # 初始化本地暫存
        self._init_cache_db()
        self._load_sync_queue()
    
    def _init_cache_db(self):
        """初始化本地暫存資料庫 SQLite"""
        conn = sqlite3.connect(CACHE_DB)
        cursor = conn.cursor()
        
        # 建立暫存資料表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intruder_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                image_path TEXT,
                image_data BLOB,
                synced BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def _load_sync_queue(self):
        """載入同步佇列 (如果存在的話)"""
        if os.path.exists(SYNC_QUEUE):
            try:
                with open(SYNC_QUEUE, 'r') as f:
                    self.queue = json.load(f)
            except:
                self.queue = []
        else:
            self.queue = []
    
    def _save_sync_queue(self):
        """儲存同步佇列到本地檔案"""
        with open(SYNC_QUEUE, 'w') as f:
            json.dump(self.queue, f)
    
    def upload_intruder_data(self, image_path=None, image_bytes=None, timestamp=None):
        """
        上傳闖入者資料到雲端
        
        參數:
            image_path: 本地照片路徑
            image_bytes: 照片的二進位資料
            timestamp: 紀錄時間戳記
        
        回傳:
            bool: 是否成功上傳
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        # 如果提供的是檔案路徑，則讀取檔案內容
        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
        
        # 第一步：先儲存到本地暫存（確保斷線也不會遺失）
        cache_id = self._cache_intruder_data(image_path, image_bytes, timestamp)
        
        # 第二步：如果目前有網路，立刻嘗試上傳
        if self.connected:
            success = self._sync_to_cloud(image_path, image_bytes, timestamp)
            if success:
                print(f"✓ 闖入者資料已成功上傳至雲端")
                if cache_id is not None:
                    # 上傳成功後，將本地紀錄標記為已同步
                    self._mark_as_synced(cache_id)
                return True
            else:
                print(f"⚠ 雲端上傳失敗，資料已安全保留於本地暫存")
                return False
        else:
            print(f"⚠ 目前無網路連線，資料已保留於本地暫存，將等待網路恢復後自動重試")
            return False
    
    def _cache_intruder_data(self, image_path, image_bytes, timestamp):
        """將闖入者資料寫入本地 SQLite 暫存"""
        try:
            conn = sqlite3.connect(CACHE_DB)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO intruder_cache (timestamp, image_path, image_data, synced)
                VALUES (?, ?, ?, 0)
            """, (timestamp, image_path or "", image_bytes))
            last_id = cursor.lastrowid
            conn.commit()
            conn.close()
            print(f"✓ 資料已安全備份至本地端")
            return last_id
        except Exception as e:
            print(f"✗ 本地備份失敗: {e}")
            return None

    def _mark_as_synced(self, record_id):
        """將本地資料庫中的該筆紀錄標記為「已同步」(synced = 1)"""
        try:
            conn = sqlite3.connect(CACHE_DB)
            cursor = conn.cursor()
            cursor.execute("UPDATE intruder_cache SET synced = 1 WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"✗ 更新同步狀態失敗: {e}")
    
    def _sync_to_cloud(self, image_path, image_bytes, timestamp):
        """實際執行將資料同步上傳到 Supabase 雲端的操作"""
        try:
            if not self.connected:
                return False
            
            # 準備要上傳的 JSON 資料結構
            record = {
                "created_at": timestamp,
                "detection_status": "intruder_detected",
                "image_data": image_bytes.hex() if image_bytes else None
            }
            
            # 執行插入資料到 Supabase
            response = self.client.table("intruder_logs").insert(record).execute()
            
            if response.data:
                print(f"✓ 紀錄已成功上傳到 Supabase (資料 ID: {response.data[0]['id']})")
                return True
            else:
                print(f"✗ Supabase 上傳失敗 (無回傳資料)")
                return False
                
        except Exception as e:
            print(f"✗ 雲端同步發生錯誤: {e}")
            return False
    
    def sync_cached_data(self):
        """
        把本地資料庫所有尚未同步的資料上傳到雲端
        (這通常由背景執行緒定期呼叫，或是網路剛恢復時呼叫)
        """
        try:
            conn = sqlite3.connect(CACHE_DB)
            cursor = conn.cursor()
            
            # 撈出所有標記為未同步 (synced = 0) 的紀錄
            cursor.execute("SELECT id, timestamp, image_data FROM intruder_cache WHERE synced = 0")
            records = cursor.fetchall()
            
            if not records:
                print("✓ 本地沒有需要補傳的暫存資料")
                return
            
            if not self.connected:
                print(f"⚠ 網路未連線，尚有 {len(records)} 筆資料等待同步")
                return
            
            synced_count = 0
            for record_id, timestamp, image_data in records:
                try:
                    cloud_record = {
                        "created_at": timestamp,
                        "detection_status": "intruder_detected",
                        "image_data": image_data.hex() if image_data else None
                    }
                    
                    response = self.client.table("intruder_logs").insert(cloud_record).execute()
                    
                    if response.data:
                        # 成功上傳後，將本地紀錄標記為已同步
                        cursor.execute("UPDATE intruder_cache SET synced = 1 WHERE id = ?", (record_id,))
                        synced_count += 1
                        print(f"✓ 成功補傳紀錄 ID: {record_id}")
                except Exception as e:
                    print(f"✗ 補傳紀錄 ID {record_id} 失敗: {e}")
            
            conn.commit()
            conn.close()
            
            if synced_count > 0:
                print(f"✓ 背景同步完成: 成功上傳 {synced_count}/{len(records)} 筆暫存資料")
            
        except Exception as e:
            print(f"✗ 執行背景同步暫存資料時發生錯誤: {e}")
    
    def check_connection(self):
        """檢查與 Supabase 的連線狀態"""
        try:
            # 嘗試讀取一筆資料來測試連線
            response = self.client.table("intruder_logs").select("id").limit(1).execute()
            self.connected = True
            # print("✓ Supabase 連線正常") # 避免背景一直洗畫面，可將此行註解
            return True
        except Exception as e:
            self.connected = False
            print(f"⚠ Supabase 連線中斷: {e}")
            return False
    
    def start_sync_worker(self, interval=60):
        """
        啟動背景自動同步的執行緒 (Worker Thread)
        
        參數:
            interval: 每次檢查的間隔時間 (秒)
        """
        def worker():
            while True:
                time.sleep(interval)
                self.check_connection()
                self.sync_cached_data()
        
        # 設定為 daemon 執行緒，主程式結束時它也會自動結束
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        print(f"✓ 已啟動背景自動同步執行緒 (檢查間隔: {interval}秒)")


# 全域實例 (Singleton)
cloud_sync = None

def init_cloud_sync():
    """初始化並啟動雲端同步功能 (供主程式呼叫)"""
    global cloud_sync
    cloud_sync = CloudSync()
    cloud_sync.start_sync_worker(interval=30)  # 每 30 秒自動檢查一次是否有需要補傳的資料
    return cloud_sync

def upload_intruder(image_path=None, image_bytes=None):
    """供主程式呼叫的便捷函式：觸發上傳闖入者資料"""
    if cloud_sync:
        return cloud_sync.upload_intruder_data(image_path, image_bytes)
    return False
