<div align="center">

# 🚪 Smart Face Recognition Door Lock
**結合邊緣運算 (Edge Computing)、AI 電腦視覺與物聯網 (IoT) 技術的智慧門鎖。**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

</div>

<br>

<details>
<summary><b>📖 點擊展開專案目錄 (Table of Contents)</b></summary>

- [🎥 成果展示 (Demo & Showcase)](#-成果展示-demo--showcase)
  - [💻 1. PC Node](#-1-pc-node)
  - [📡 2. 樹莓派終端設備 (Raspberry Pi Node)](#-2-樹莓派終端設備-raspberry-pi-node)
- [🗺️ 系統圖解 (System Diagrams)](#️-系統圖解-system-diagrams)
  - [1. 系統完整流程圖 (System Flowchart)](#1-系統完整流程圖-system-flowchart)
  - [2. 硬體接線圖 (Wiring Diagram)](#2-硬體接線圖-wiring-diagram)
  - [3. Zero 2w 腳位圖](#3-zero-2w-腳位圖)
- [✨ 系統核心功能與技術優勢 (Core Features & Technical Advantages)](#-系統核心功能與技術優勢-core-features--technical-advantages)
  - [🖐️ 電腦視覺低功耗喚醒機制](#️-電腦視覺低功耗喚醒機制)
  - [🧠 雙引擎深度學習人臉辨識](#-雙引擎深度學習人臉辨識)
  - [☁️ 邊緣與雲端協同即時監控](#️-邊緣與雲端協同即時監控)
  - [📶 高強健性非同步容錯傳輸](#-高強健性非同步容錯傳輸)
  - [🔄 自適應白名單特徵擴充](#-自適應白名單特徵擴充)
- [🏗️ 系統架構 (System Architecture)](#️-系統架構-system-architecture)
  - [📡 終端設備端 (Raspberry Pi Zero 2 WH)](#-終端設備端-raspberry-pi-zero-2-wh)
  - [💻 核心運算端 (PC)](#-核心運算端-pc)
- [📂 專案目錄結構 (Project Structure)](#-專案目錄結構-project-structure)
- [🛡️ 安全防護與雲端整合 (Security & Cloud)](#️-安全防護與雲端整合-security--cloud)
- [⚙️ 環境與硬體準備 (Environment & Hardware Setup)](#️-環境與硬體準備-environment--hardware-setup)
  - [【PC 端】核心大腦](#pc-端核心大腦)
  - [【樹莓派端】眼睛與手](#樹莓派端眼睛與手)
- [🚀 系統部署與啟動](#-系統部署與啟動)
  - [步驟 1：同步程式碼至邊緣端](#步驟-1同步程式碼至邊緣端)
  - [步驟 2：依序啟動系統](#步驟-2依序啟動系統)
- [🛠️ 維護與測試 (Maintenance & Testing)](#️-維護與測試-maintenance--testing)
- [📦 物料清單 (BOM)](#-物料清單-bom)
- [👥 團隊成員 (Team Members)](#-團隊成員-team-members)

</details>

---

## 🎥 成果展示 (Demo & Showcase)

運行成果分為 **PC 核心運算端** 與 **樹莓派邊緣終端** 進行圖文對照。

### 💻 1. PC Node


| 🚪 實體開門作動  | 📡 即時影像監控串流 |
| :---: | :---: |
| <img src="docs/images/motor_action.gif" width="400" alt="馬達轉動畫面"> | <img src="https://github.com/user-attachments/assets/9c8f5fee-e40e-4ea5-92ef-6c38fdc23ed2" width="400" alt="PC端顯示樹梅派的相機畫面"> |
| *驗證成功後，發送指令驅動馬達將推開* | *PC 端即時接收並顯示來自門外樹莓派的 TCP 影像* |
| ✅ 辨識成功  | ❌ 異常攔截 |
| <img src="https://github.com/user-attachments/assets/80b85d77-0145-4645-b077-9794b14251f1" width="400" alt="成功辨別是主人"> | <img src="https://github.com/user-attachments/assets/1c32897d-4bc3-4983-9333-9518247a86f4" width="400" alt="成功辨別非主人"> |
| *成功辨識臉部特徵，顯示高置信度並亮起綠燈觸發開門* | *偵測到非白名單人臉，拒絕開門並觸發現場抓拍與雲端上傳* |




### 📡 2. 樹莓派終端設備 (Raspberry Pi Node)

**🍓 樹莓派硬體與推門機構整體外觀**  
<br>
<img src="docs/images/pi_hardware_setup.jpg" width="800" alt="樹梅派整體外觀">  
> *Pi Zero 2 WH、攝影機、步進馬達與 ULN2003 驅動板的實體組裝外觀 ）*

<br>

| 🔌 接收馬達驅動訊號 | 👁️ 攝影機 TCP 連線監聽狀態 |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/126b227b-0d46-4c87-b6c6-c0394cf4d281" width="400" alt="接收到馬達的訊號"> | <img src="https://github.com/user-attachments/assets/8bf7d43e-f972-43d8-9358-dd8468756bba" width="400" alt="接收監聽訊號"> |
| *終端機日誌：顯示成功接收 PC 端開門指令，準備驅動 GPIO* | *終端機日誌：建立 TCP 連線，持續推播影像並監聽回傳訊號* |

---

### ☁️ 3. Supabase 雲端資料庫紀錄 (Supabase Cloud Storage & Database)

**📊 闖入者日誌與影像紀錄**  
<br>

| 📝 闖入者 Log 訊息紀錄 | 📸 闖入者影像照片 |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/0abd451e-686f-4d92-b985-6efd1f8c2240" width="400" alt="Supabase Log 紀錄訊息"> | <img src="https://github.com/user-attachments/assets/e38e38ea-110d-40ca-bb12-a2bdaba77342" width="400" alt="Supabase 闖入者照片"> |
| *Supabase Database：詳細記錄闖入事件發生的時間點與相關狀態* | *Supabase Storage：自動捕捉並上傳至雲端的闖入者截圖* |

---

## 🗺️ 系統圖解 (System Diagrams)

### 1. 系統完整流程圖 (System Flowchart)
![系統完整流程圖](https://github.com/user-attachments/assets/79b8c8f4-c69f-437c-8303-bba2c38018c1)
> *說明：展示從手勢喚醒、影像強化、ArcFace + Facenet 雙重 AI 辨識，到最終實體作動與 Supabase 雲端上傳的完整生命週期。*

### 2. 硬體接線圖 (Wiring Diagram)
![樹梅派與馬達的接線圖](https://github.com/user-attachments/assets/bb6aed93-86ad-45ff-b776-3aa623d10df4)
> *說明：Raspberry Pi Zero 2 WH 與 ULN2003 步進馬達驅動板的詳細 GPIO 接線配置。*

### 3. Zero 2w 腳位圖
![樹梅派與馬達的接線圖](https://github.com/user-attachments/assets/946e4078-6b62-4b7a-97ff-bac6b208822a)
> *說明：Raspberry Pi Zero 2 WH 的針腳位置參考。*

---

## ✨ 系統核心功能與技術優勢 (Core Features & Technical Advantages)

### 🖐️ 電腦視覺低功耗喚醒機制
> **Vision-Based Low-Power Wake-up Mechanism**

* **運作機制**：系統常態維持極低能耗待機，透過輕量級手勢偵測模型，使用者僅需出示特定手勢（如單指特徵）即可觸發瞬時喚醒。
* **系統優勢**：將運算資源由休眠狀態無縫切換至全域辨識模式，大幅提升整體邊緣設備的能源使用效益。

---

### 🧠 雙引擎深度學習人臉辨識
> **Dual-Engine Deep Learning Facial Recognition**

* **核心技術**：ArcFace + Facenet 雙軌驗證、CLAHE 動態影像強化。
* **運作機制**：於特徵擷取前導入影像強化技術，克服背光與低照度環境干擾，再透過雙軌演算法進行特徵比對。
* **系統優勢**：複合架構確保了極高的生物特徵比對精準度，建構出高容錯率的安全防護網。

---

### ☁️ 邊緣與雲端協同即時監控
> **Edge-Cloud Collaborative Security Monitoring**

* **核心技術**：Supabase 雲端基礎設施。
* **運作機制**：當系統偵測並攔截非授權之人臉特徵（異常闖入者）時，將立即觸發邊緣端影像擷取。
* **系統優勢**：將未授權事件及影像紀錄即時推播至雲端資料庫，建立嚴密的存取稽核機制，實現零時差遠端監控。

---

### 📶 高強健性非同步容錯傳輸
> **Robust Asynchronous Fault-Tolerant Transmission**

* **核心技術**：SQLite 本地快取層 (Local Cache Layer)、背景非同步執行緒。
* **運作機制**：遭遇網路連線中斷時，存取日誌與抓拍檔案將進行本地安全落地；待網路拓樸恢復，系統即自動進行非同步資料補傳。
* **系統優勢**：有效克服實務物聯網場域中潛在的網路波動，確保所有稽核紀錄零遺漏。

---

### 🔄 自適應白名單特徵擴充
> **Adaptive Whitelist Feature Expansion Algorithm**

* **核心技術**：持續性學習 (Continuous Learning)。
* **運作機制**：針對日常高置信度（High Confidence）的辨識結果進行特徵萃取，並動態將其擴充至本地授權白名單資料庫中。
* **系統優勢**：系統能隨著時間推移與日常使用，穩步優化辨識演算法之效率與整體使用者體驗。

---

## 🏗️ 系統架構 (System Architecture)

**主從式架構 (Client-Server Architecture)**，將輕量控制與繁重運算分工：

### 📡 終端設備端 (Raspberry Pi Zero 2 WH)
部署於門邊，作為系統的「眼睛與手」。
*   **影像擷取**：透過攝影機捕捉即時影像。
*   **低延遲傳輸**：利用 TCP 協定將影像串流至室內運算中心。
*   **實體控制**：接收驗證通過指令，驅動步進馬達完成「向後推開」的物理開門動作。

### 💻 核心運算端 (PC)
部署於室內，作為系統的「大腦」。
1.  **手勢喚醒**：偵測到特定手勢後啟動辨識流程。
2.  **特徵鎖定與強化**：喚醒 MediaPipe 鎖定臉部特徵，並立刻進行影像強化 (CLAHE) 克服光線干擾。
3.  **雙重辨識 (ArcFace + Facenet)**：先以 ArcFace 進行快速高精度的判定；若遇邊緣數值，無縫啟動 Facenet 進行二次確認。


## 📂 專案目錄結構 (Project Structure)

```text
📦 Smart-Face-Lock
 ┣ 📂 pc_node/                 # 電腦端：核心運算與 AI 辨識
 ┃ ┣ 📂 owners/                # 存放白名單人臉照片 (需自行建立)
 ┃ ┣ 📂 intruders/             # 存放被攔截的陌生人抓拍 (自動生成)
 ┃ ┣ 📜 pc_gesture.py          # 電腦端主程式 (手勢喚醒 + 人臉辨識)
 ┃ ┗ 📜 requirements.txt       # PC 端相依套件清單
 ┣ 📂 pi_node/                 # 樹莓派端：邊緣終端與馬達控制
 ┃ ┣ 📜 pi_motor_server.py     # 接收開門指令與馬達驅動
 ┃ ┗ 📜 pi_stream_client.py    # 影像擷取與 TCP 串流推播
 ┣ 📂 AWS/                     # 部署腳本與自動化工具
 ┣ 📜 .env.example             # 環境變數範例檔
 ┗ 📜 README.md
```
---

## 🛡️ 安全防護與雲端整合 (Security & Cloud)

安全機制：

| 防護機制 | 運作說明 |
| :--- | :--- |
| **🚨 陌生人攔截抓拍** | 辨識到非白名單臉孔時，系統將立即拒絕開門，並自動拍下現場照片。 |
| **☁️ 雲端即時上傳** | 透過整合 **Supabase** 服務，將影像與存取日誌即時推播至雲端，方便遠端監控。 |
| **💾 離線快取機制** | 因應真實場景的網路不穩，內建 **SQLite** 進行本地端備份。斷網時安全記錄不遺失，網路恢復即自動補傳。 |

---

## ⚙️ 環境與硬體準備 (Environment & Hardware Setup)

### 【PC 端】核心大腦
* **網路設定**：預設 IP 為 `192.168.0.148`，需與樹莓派處於同一個區域網路。
* **軟體依賴**：需確保安裝專案所需的 Python 套件，包含 OpenCV、mediapipe、deepface 與 supabase 等。
* **環境建置**：請確認雲端 Supabase 專案環境與金鑰已設定完成。
* **權限目錄**：需在專案內建立 `owners/` 資料夾，並放置可通行者的清晰正臉照片作為白名單。

### 【樹莓派端】眼睛與手
* **網路設定**：預設 IP 為 `192.168.0.192`。
* **硬體連接**：WebCam 需正確接上樹莓派的 USB 埠。
* **機構控制**：步進馬達（含 ULN2003 驅動板）的腳位需連接至 GPIO 17, 18, 27, 22。系統設計為收到指令後，馬達會**推開門片**。

---

## 🚀 系統部署與啟動

### 步驟 1：同步程式碼至邊緣端
若 PC 端有修改樹莓派腳本，進入 `AWS/` 資料夾執行 `upload_all_to_pi.bat`，系統會透過 SCP 自動上傳檔案。接著執行 `ssh_to_pi.bat` 登入樹莓派終端機。

### 步驟 2：依序啟動系統 
為確保 TCP Socket 通訊正常，遵守以下順序：

| 順序 | 執行設備 | 終端機指令 | 狀態說明 |
| :---: | :--- | :--- | :--- |
| **1** | 🍓 樹莓派 | `python pi_motor_server.py` | 開啟 Port `65432`，等待接收 PC 端的開門指令 |
| **2** | 💻 PC 端 | `python pc_gesture.py` | 開啟 Port `65434` 等待影像，並主動連線至樹莓派控制馬達 |
| **3** | 🍓 樹莓派 | `python pi_stream_client.py` | *(開啟第二個終端機)* 啟動相機並將影像串流推播至 PC 端 |

---

## 🛠️ 維護與測試 (Maintenance & Testing)

* **單獨測試實體門鎖**：SSH 登入樹莓派，執行 `python test_motor.py`，觀察馬達是否正常將門往後推開。
* **新增/移除權限**：只需在 PC 端的 `owners/` 資料夾內新增或刪除臉孔照片。再次喚醒系統時，權限即會更新。
* **查看闖入紀錄**：前往 PC 端 `intruders/` 資料夾，即可檢視所有未通過驗證（被拒絕開門）的闖入者擷圖。

---

## 📦 物料清單 (BOM)

| 零件名稱 (Component) | 規格/型號 | 備註說明 |
| :--- | :--- | :--- |
| **邊緣運算板** | Raspberry Pi Zero 2 WH | 輕量化終端，負責影像串流與馬達控制 |
| **攝影鏡頭** | 兼容之 WebCam 或 Pi Camera | 安裝於門外，擷取人臉與手勢 |
| **步進馬達** | 5V 步進馬達 | 負責將門片向後推開的物理作動 |
| **馬達驅動板** | ULN2003 | 接收 Zero 2 WH GPIO 訊號以驅動馬達 |
| **電源供應器** | Pi Zero 2 W 專屬電源 | 提供邊緣運算板穩定供電 |
| **儲存與燒錄** | SD卡 + SD卡讀卡機 | 用於燒錄樹莓派 OS 與存放終端程式碼 |
| **轉接配件** | Micro USB 轉接頭 | 用於 Zero 2 WH 連接周邊設備 (如鏡頭) |
| **轉接配件** | Micro HDMI 轉接頭 | 用於 Zero 2 WH 連接螢幕進行初期設定 |
| **周邊耗材** | 杜邦線 | 用於連接 GPIO 腳位與驅動板 |

---

## 👥 團隊成員 (Team Members)


| 名字 (Name) | 學號 (Student ID) |
| :---: | :---: |
| 羅奕程 | M11451021 |
| 王建傑 | M11451009 |
| 吳宗韓 | M11451019 |
| Peeranut Wiwarrawornchai | M11451801 |

