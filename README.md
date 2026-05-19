# 🚪 Smart Face Recognition Door Lock 

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

> **結合邊緣運算 (Edge Computing)、AI 電腦視覺與物聯網 (IoT) 技術的現代化智慧門鎖解決方案。**

---

## 🎥 成果展示 (Demo & Showcase)

*(在此替換為您的專案展示 GIF 或 YouTube 影片連結)*
![System Demo](https://via.placeholder.com/800x400?text=Insert+Demo+GIF+Here)

**展示亮點：**
* 👆 **一指喚醒：** 待機狀態下比出單指手勢，系統瞬間啟動。
* ⚡ **極速辨識：** ArcFace + Facenet 雙引擎，無感延遲完成驗證。
* 🚪 **實體作動：** 驗證通過後，步進馬達精準驅動，門片平穩地**往後推開**，實現真正的無接觸通行。
* 🚨 **異常攔截：** 陌生人臉測試，立即亮紅燈拒絕並完成抓拍上傳。

---

## ✨ 核心特色 (Key Features)

*   🖐️ **創新「手勢喚醒」機制**：系統平時處於低耗能待機狀態。只需對鏡頭比出特定手勢（伸出一根手指），即可瞬間喚醒系統，兼顧環保與效能。
*   🧠 **雙重 AI 高精度辨識**：首創 ArcFace 搭配 Facenet 的雙引擎架構，結合動態影像強化技術，打造極高準確率與零死角的安全防護。
*   ☁️ **雲端守衛與即時監控**：整合 Supabase 雲端服務，陌生闖入者無所遁形，即時抓拍並上傳雲端。
*   📶 **強韌的斷網離線機制**：內建 SQLite 本地快取，即使網路斷線也能確實記錄，網路恢復後自動於背景補傳，居家安全滴水不漏。
*   🔄 **智慧白名單學習**：系統具備「自動學習」功能，能將高置信度的臉部資料自動存入白名單，讓日常開門體驗越來越順暢。

---

## 🏗️ 系統架構 (System Architecture)

**主從式架構 (Client-Server Architecture)**，將輕量控制與繁重運算分工：

### 📡 終端設備端 (Raspberry Pi)
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

## 🔄 系統流程 (System Flow)

1. **待機模式 (Standby)**：樹莓派持續擷取低幀率影像，系統處於低耗能狀態。
2. **手勢喚醒 (Wake-up)**：使用者於鏡頭前比出「單指」，PC 端 MediaPipe 偵測後喚醒主系統。
3. **影像優化 (Enhancement)**：擷取臉部特徵，自動執行 CLAHE 演算法處理光線反差。
4. **AI 雙重辨識 (Verification)**：
   * 進入 **ArcFace** 模型進行第一階段高精度比對。
   * 若信心分數落於邊緣閾值，自動觸發 **Facenet** 進行二次確認。
5. **結果判定 (Decision)**：
   * ✅ **驗證成功**：傳送開門訊號至樹莓派 -> 驅動步進馬達將門向後推開 -> 高置信度特徵自動學習更新至白名單。
   * ❌ **驗證失敗**：拒絕開門 -> 觸發相機抓拍 -> 寫入 SQLite 本地紀錄 -> 背景同步上傳至 Supabase 雲端。

---

## 🔌 馬達接線圖 (Motor Wiring Diagram)

為了實現門片向後推開的物理作動，本專案使用步進馬達搭配驅動板（以 ULN2003 / A4988 為例）連接至 Raspberry Pi：

*(請將下方替換為實際的 Fritzing 圖片或電路圖)*
![Wiring Diagram](https://via.placeholder.com/800x400?text=Insert+Wiring+Diagram+Here)

| Raspberry Pi (GPIO) | 步進馬達驅動板 | 說明 |
| :--- | :--- | :--- |
| 5V (Pin 2 / 4) | VCC / VMOT | 提供馬達驅動電源 |
| GND (Pin 6) | GND | 共地 |
| GPIO 17 (Pin 11) | IN1 / STEP | 控制步進訊號 |
| GPIO 18 (Pin 12) | IN2 / DIR | 控制旋轉方向（負責向後推開與復位） |
| GPIO 27 (Pin 13) | IN3 | - |
| GPIO 22 (Pin 15) | IN4 | - |

> **設計巧思：** 馬達透過特製的連桿與鉸鏈機構連接門片，確保扭力足以穩定將門往後推開，並在設定時間後自動反轉關上。

---

## 📦 物料清單 (BOM)

| 零件名稱 (Component) | 規格/型號 | 數量 | 備註說明 |
| :--- | :--- | :--- | :--- |
| **運算主機 (PC)** | 具備獨立顯卡佳 | 1 | 負責執行 AI 雙重辨識與影像優化 |
| **邊緣運算板** | Raspberry Pi 4 Model B | 1 | 負責影像串流、控制馬達與接收訊號 |
| **攝影鏡頭** | 1080p USB WebCam | 1 | 安裝於門外，擷取人臉與手勢 |
| **步進馬達** | 28BYJ-48 或 NEMA 17 | 1 | 依實際門片重量選擇對應扭力之型號 |
| **馬達驅動板** | ULN2003 或 A4988 | 1 | 接收樹莓派訊號以驅動馬達 |
| **電源供應器** | 5V/3A (供樹莓派) & 12V (供馬達) | 1 | 確保硬體穩定運作 |
| **周邊耗材** | 杜邦線、麵包板、門片連桿機構 | 一式 | 實作推門機關之物理結構 |

---

## 👥 團隊成員 (Team Members)

* **[您的名字/姓名 1]** - *專案發起、架構設計、AI 辨識模型整合* - [GitHub](https://github.com/yourusername)
* **[姓名 2]** - *樹莓派邊緣運算、TCP 影像串流與馬達控制* - [GitHub](https://github.com/member2)
* **[姓名 3]** - *Supabase 雲端資料庫與 SQLite 離線快取串接* - [GitHub](https://github.com/member3)
