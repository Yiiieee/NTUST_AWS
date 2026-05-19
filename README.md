# 🚪 Smart Face Recognition Door Lock 

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

> **結合邊緣運算 (Edge Computing)、AI 電腦視覺與物聯網 (IoT) 技術的現代化智慧門鎖解決方案。**

---

## 🎥 成果展示 (Demo & Showcase)

為了讓展示更直觀，以下將實際運行成果分為 **PC 核心運算端** 與 **樹莓派邊緣終端** 進行圖文對照。

### 💻 1. PC 端運算與監控中心 (PC Node)

| 🚪 實體開門作動 (GIF) | 📡 即時影像監控串流 |
| :---: | :---: |
| <img src="docs/images/motor_action.gif" width="400" alt="馬達轉動畫面"> | <img src="docs/images/pc_camera_stream.jpg" width="400" alt="PC端顯示樹梅派的相機畫面"> |
| *驗證成功後，發送指令驅動馬達將門平穩**向後推開**的作動畫面* | *PC 端即時接收並顯示來自門外樹莓派的 TCP 低延遲影像* |
| **✅ 辨識成功 (主人/白名單)** | **❌ 異常攔截 (陌生人/非白名單)** |
| <img src="docs/images/auth_success.jpg" width="400" alt="成功辨別是主人"> | <img src="docs/images/auth_failed.jpg" width="400" alt="成功辨別非主人"> |
| *成功辨識主人臉部特徵，顯示高置信度並亮起綠燈觸發開門* | *偵測到非白名單人臉，拒絕開門並觸發現場抓拍與雲端上傳* |

### 📡 2. 樹莓派終端設備 (Raspberry Pi Node)

**🍓 樹莓派硬體與推門機構整體外觀**  
<img src="docs/images/pi_hardware_setup.jpg" width="800" alt="樹梅派整體外觀">  
> *Pi Zero 2 WH、攝影機、步進馬達與 ULN2003 驅動板的實體組裝外觀（包含向後推開的門片機構）*

<br>

| 🔌 接收馬達驅動訊號 | 👁️ 攝影機 TCP 連線監聽狀態 |
| :---: | :---: |
| <img src="docs/images/pi_motor_signal.jpg" width="400" alt="接收到馬達的訊號"> | <img src="docs/images/pi_camera_listening.jpg" width="400" alt="接收監聽訊號"> |
| *終端機日誌：顯示成功接收 PC 端開門指令，準備驅動 GPIO* | *終端機日誌：建立 TCP 連線，持續推播影像並監聽回傳訊號* |

*(註：請將上述圖片替換為實際拍攝的檔案，並放於 `docs/images/` 目錄下)*

---

## 🗺️ 系統圖解 (System Diagrams)

### 1. 系統完整流程圖 (System Flowchart)
![系統完整流程圖](docs/images/system_flowchart.png)
> *說明：展示從手勢喚醒、影像強化、ArcFace + Facenet 雙重 AI 辨識，到最終實體作動與 Supabase 雲端上傳的完整生命週期。*

### 2. 硬體接線圖 (Wiring Diagram)
![樹梅派與馬達的接線圖](docs/images/wiring_diagram.png)
> *說明：Raspberry Pi Zero 2 WH 與 ULN2003 步進馬達驅動板的詳細 GPIO 接線配置，負責實現門片向後推開的物理機構設計。*

---

## ✨ 具備的功能

*   🖐️ **創新「手勢喚醒」機制**：系統平時處於低耗能待機狀態。只需對鏡頭比出特定手勢（伸出一根手指），即可瞬間喚醒系統，兼顧環保與效能。
*   🧠 **雙重 AI 高精度辨識**：首創 ArcFace 搭配 Facenet 的雙引擎架構，結合動態影像強化技術，打造極高準確率與零死角的安全防護。
*   ☁️ **雲端守衛與即時監控**：整合 Supabase 雲端服務，陌生闖入者無所遁形，即時抓拍並上傳雲端。
*   📶 **強韌的斷網離線機制**：內建 SQLite 本地快取，即使網路斷線也能確實記錄，網路恢復後自動於背景補傳，居家安全滴水不漏。
*   🔄 **智慧白名單學習**：系統具備「自動學習」功能，能將高置信度的臉部資料自動存入白名單，讓日常開門體驗越來越順暢。

---

## 🏗️ 系統架構 (System Architecture)

**主從式架構 (Client-Server Architecture)**，將輕量控制與繁重運算分工：

### 📡 終端設備端 (Raspberry Pi Zero 2 WH)
部署於門邊，作為系統的「眼睛與手」。
*   **影像擷取**：透過攝影機捕捉即時影像。
*   **低延遲傳輸**：利用 TCP 協定將影像串流至室內運算中心。
*   **實體控制**：接收驗證通過指令，驅動步進馬達完成「實體開門」動作。

### 💻 核心運算端 (PC)
部署於室內，作為系統的「大腦」。
1.  **手勢喚醒**：偵測到特定手勢後啟動辨識流程。
2.  **特徵鎖定與強化**：喚醒 MediaPipe 鎖定臉部特徵，並立刻進行影像強化 (CLAHE) 克服光線干擾。
3.  **雙重辨識 (ArcFace + Facenet)**：先以 ArcFace 進行快速高精度的判定；若遇邊緣數值，無縫啟動 Facenet 進行二次確認。

---

## 🛡️ 安全防護與雲端整合 (Security & Cloud)

安全機制：

| 防護機制 | 運作說明 |
| :--- | :--- |
| **🚨 陌生人攔截與抓拍** | 辨識到非白名單臉孔（闖入者）時，系統將立即拒絕開門，並自動拍下高清現場照片。 |
| **☁️ 雲端即時上傳** | 透過整合 **Supabase** 服務，將影像與存取日誌即時推播至雲端，方便遠端監控。 |
| **💾 離線快取機制** | 因應真實場景的網路不穩，內建 **SQLite** 進行本地端備份。斷網時安全記錄不遺失，網路恢復即自動補傳。 |

---

## 📦 物料清單 (BOM)

| 零件名稱 (Component) | 規格/型號 | 數量 | 備註說明 |
| :--- | :--- | :--- | :--- |
| **運算主機 (PC)** | 具備獨立顯卡佳 | 1 | 負責執行 AI 雙重辨識與核心運算 |
| **邊緣運算板** | Raspberry Pi Zero 2 WH | 1 | 輕量化終端，負責影像串流與馬達控制 |
| **攝影鏡頭** | 兼容之 WebCam 或 Pi Camera | 1 | 安裝於門外，擷取人臉與手勢 |
| **步進馬達** | 5V 步進馬達 | 1 | 負責將門片往後推開的物理作動 |
| **馬達驅動板** | ULN2003 | 1 | 接收 Zero 2 WH GPIO 訊號以驅動馬達 |
| **電源供應器** | Pi Zero 2 W 專屬電源 | 1 | 提供邊緣運算板穩定供電 |
| **儲存與燒錄** | SD卡 + SD卡讀卡機 | 1 套 | 用於燒錄樹莓派 OS 與存放終端程式碼 |
| **轉接配件** | Micro USB 轉接頭 | 1 | 用於 Zero 2 WH 連接周邊設備 (如鏡頭) |
| **轉接配件** | Micro HDMI 轉接頭 | 1 | 用於 Zero 2 WH 連接螢幕進行初期設定 |
| **周邊耗材** | 杜邦線 | 數條 | 用於連接 GPIO 腳位與驅動板 |

---

## 👥 團隊成員 (Team Members)

* **[您的名字/姓名 1]** - *專案發起、架構設計、AI 辨識模型整合* - [GitHub](https://github.com/yourusername)
* **[姓名 2]** - *樹莓派邊緣運算、TCP 影像串流與馬達控制* - [GitHub](https://github.com/member2)
* **[姓名 3]** - *Supabase 雲端資料庫與 SQLite 離線快取串接* - [GitHub](https://github.com/member3)
