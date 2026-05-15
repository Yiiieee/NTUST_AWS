

from supabase import create_client, Client

SUPABASE_URL = "https://iyzkimsbcvzxzhbvvlrf.supabase.co"
SUPABASE_KEY = "sb_publishable_9UyTV4wxUCkC2jwqTpSsoQ_91b64QoX"

def setup_supabase():
    """初始化 Supabase"""
    try:
        client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✓ 成功連線至 Supabase")
        
        # 测试连接
        response = client.table("intruder_logs").select("*").limit(1).execute()
        print("✓ intruder_logs 表已存在")
        print("✓ 表结构已准备好，可以开始上传不匹配的闯入者数据")
        
        return True
        
    except Exception as e:
        print(f"✗ 連線失敗: {e}")
        
        
        sql = """-- 建立闯入者紀錄表（只存储不匹配的数据）
CREATE TABLE IF NOT EXISTS intruder_logs (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    created_at TIMESTAMP DEFAULT now(),
    image_data TEXT,
    detection_status VARCHAR(50) DEFAULT 'intruder_detected',
    updated_at TIMESTAMP DEFAULT now()
);

-- 禁用 RLS，允许所有操作
ALTER TABLE intruder_logs DISABLE ROW LEVEL SECURITY;"""
        
        return False

if __name__ == "__main__":
    setup_supabase()
    print("\n✓ Supabase 初始化完成！")
