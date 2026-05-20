<div align="center">

# 🚪 Smart Face Recognition Door Lock
**A smart door lock combining Edge Computing, AI Computer Vision, and Internet of Things (IoT) technologies.**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

</div>

<br>

<details>
<summary><b>📖 Click to expand Table of Contents</b></summary>

- [🛠️ Technical Architecture & Core Highlights](#️-technical-architecture--core-highlights)
  - [💡 Core Highlights](#-core-highlights)
  - [📊 Architecture Summary](#-architecture-summary)
- [🎥 Demo & Showcase](#-demo--showcase)
  - [💻 1. PC Node](#-1-pc-node)
  - [📡 2. Raspberry Pi Node](#-2-raspberry-pi-node)
  - [☁️ 3. Supabase Cloud Storage & Database](#️-3-supabase-cloud-storage--database)
- [🗺️ System Diagrams](#️-system-diagrams)
  - [1. System Flowchart](#1-system-flowchart)
  - [2. Wiring Diagram](#2-wiring-diagram)
  - [3. Zero 2W Pinout Diagram](#3-zero-2w-pinout-diagram)
- [🔄 Adaptive Whitelist Feature Expansion](#-adaptive-whitelist-feature-expansion)
- [🏗️ System Architecture](#️-system-architecture)
  - [📡 Edge Node](#-edge-node)
  - [💻 Core Computing Node](#-core-computing-node)
- [📂 Project Structure](#-project-structure)
- [🛡️ Security & Cloud Integration](#️-security--cloud-integration)
- [⚙️ Environment & Hardware Setup](#️-environment--hardware-setup)
  - [【PC Node】 Core Brain](#pc-node-core-brain)
  - [【Raspberry Pi Node】 Eyes and Hands](#raspberry-pi-node-eyes-and-hands)
- [🚀 System Deployment & Startup](#-system-deployment--startup)
  - [Step 1: Sync Code to Edge Node](#step-1-sync-code-to-edge-node)
  - [Step 2: Sequential System Startup](#step-2-sequential-system-startup)
- [🛠️ Maintenance & Testing](#️-maintenance--testing)
- [📦 Bill of Materials](#-bill-of-materials)
- [👥 Team Members](#-team-members)

</details>

## 🛠️ Technical Architecture & Core Highlights

This system integrates edge computing, dual-track deep learning recognition, and edge-cloud collaborative mechanisms to build a smart IoT security defense system with high energy efficiency, exceptional precision, and robust fault tolerance.

---

### 💡 Core Highlights

> ### 🖐️ Vision-Driven Low-Power Wake-Up
> - **Core Tech:** Lightweight Edge Gesture Detection Model
> - **Mechanism:** The system typically idles in an ultra-low-power standby mode. Upon detecting specific hand gestures (e.g., a raised index finger) via the lightweight edge model, it instantly triggers a full-system wake-up.
> - **Advantage:** Seamlessly transitions computing resources from sleep to high-performance recognition mode, drastically optimizing the edge device's overall energy efficiency.
>
> ---
>
> ### 🧠 Dual-Engine Deep Learning Facial Recognition
> - **Core Tech:** ArcFace + FaceNet dual-track cross-verification, CLAHE dynamic image enhancement.
> - **Mechanism:** Applies CLAHE prior to feature extraction to overcome backlight and low-light interference, followed by a dual-track algorithmic approach for feature matching and cross-verification.
> - **Advantage:** This composite architecture guarantees exceptional biometric accuracy, establishing a highly resilient security perimeter.
>
> ---
>
> ### ☁️ Edge-Cloud Collaborative Security Monitoring
> - **Core Tech:** Supabase Cloud Infrastructure
> - **Mechanism:** Instantly captures images and triggers alerts at the edge node whenever unauthorized facial features (e.g., unverified intruders) are intercepted.
> - **Advantage:** Pushes real-time alerts and audit logs to the cloud database, establishing a strict access control system with zero-latency remote monitoring.
>
> ---
>
> ### 📶 Robust Asynchronous Fault-Tolerant Transmission
> - **Core Tech:** SQLite local cache layer, background asynchronous threads.
> - **Mechanism:** During network disruptions, access logs and captured media are safely cached locally. Once connectivity is restored, the system automatically executes asynchronous data retransmission in the background.
> - **Advantage:** Effectively navigates network fluctuations common in IoT environments, guaranteeing 100% data integrity and zero loss of audit records.

---

### 📊 Architecture Summary

| Module | Core Tech | Key Benefit | Design Focus |
| :--- | :--- | :--- | :--- |
| **Low-Power Wake-Up** | Lightweight Edge Gesture Model | Drastically extends battery life | Green computing, extreme energy saving |
| **Facial Recognition** | ArcFace + FaceNet + CLAHE | Overcomes extreme lighting, high accuracy | Dual-track verification, high fault tolerance |
| **Edge-Cloud Sync** | Supabase Cloud | Sub-second anomaly alerts & event tracking | Zero-latency monitoring, security auditing |
| **Fault-Tolerant Tx** | SQLite + Async Threads | Auto-resume upon reconnection, prevents data loss | 100% data integrity |

## 🎥 Demo & Showcase

The operation results are visually compared between the **PC Core Computing Node** and the **Raspberry Pi Edge Node**.

### 💻 1. PC Node


| 🚪 Physical Door Action | 📡 Real-time Video Stream Monitoring |
| :---: | :---: |
| <img src="docs/images/motor_action.gif" width="400" alt="Motor action gif"> | <img src="https://github.com/user-attachments/assets/9c8f5fee-e40e-4ea5-92ef-6c38fdc23ed2" width="400" alt="PC displays Raspberry Pi camera feed"> |
| *After successful verification, sends command to drive the motor to push the door open* | *PC node receives and displays TCP video stream from the Raspberry Pi outside the door in real-time* |
| ✅ Recognition Successful | ❌ Intruder Interception |
| <img src="https://github.com/user-attachments/assets/80b85d77-0145-4645-b077-9794b14251f1" width="400" alt="Successfully recognized as owner"> | <img src="https://github.com/user-attachments/assets/1c32897d-4bc3-4983-9333-9518247a86f4" width="400" alt="Successfully recognized as non-owner"> |
| *Successfully recognizes facial features, displays high confidence, and lights up green to trigger door opening* | *Detects non-whitelist face, refuses to open the door, and triggers site capture and cloud upload* |




### 📡 2. Raspberry Pi Node

**🍓 Overall appearance of Raspberry Pi hardware and door-pushing mechanism**  
<br>
<img src="docs/images/pi_hardware_setup.jpg" width="800" alt="Overall appearance of Raspberry Pi">  
> *(Physical assembly appearance of Pi Zero 2 WH, camera, stepper motor, and ULN2003 driver board)*

<br>

| 🔌 Receiving Motor Drive Signal | 👁️ Camera TCP Connection Listening Status |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/126b227b-0d46-4c87-b6c6-c0394cf4d281" width="400" alt="Receiving signal from motor"> | <img src="https://github.com/user-attachments/assets/8bf7d43e-f972-43d8-9358-dd8468756bba" width="400" alt="Listening to return signal"> |
| *Terminal Log: Shows successful receipt of the door-opening command from the PC node, ready to drive GPIO* | *Terminal Log: TCP connection established, continuously streaming video and listening for return signals* |

---

### ☁️ 3. Supabase Cloud Storage & Database

**📊 Intruder Logs and Image Records**  
<br>

| 📝 Intruder Log Message Records | 📸 Intruder Captured Photos |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/0abd451e-686f-4d92-b985-6efd1f8c2240" width="400" alt="Supabase Log messages"> | <img src="https://github.com/user-attachments/assets/e38e38ea-110d-40ca-bb12-a2bdaba77342" width="400" alt="Supabase Intruder Photos"> |
| *Supabase Database: Detailed records of the time and related status of intrusion events* | *Supabase Storage: Automatically captures and uploads intruder screenshots to the cloud* |

---

## 🗺️ System Diagrams

### 1. System Flowchart
![System Flowchart](https://github.com/user-attachments/assets/dc2e7bb6-07af-4c1f-b153-2d094064efb9)
> *Description: Demonstrates the complete life cycle from gesture wake-up, image enhancement, ArcFace + Facenet dual AI recognition, to final physical action and Supabase cloud upload.*

### 2. Wiring Diagram
![Wiring Diagram between Raspberry Pi and Motor](https://github.com/user-attachments/assets/267edc6a-3bf9-47bf-87c8-c79290d8395a)
> *Description: Detailed GPIO wiring configuration for Raspberry Pi Zero 2 WH and ULN2003 stepper motor driver board.*

### 3. Zero 2W Pinout Diagram
![Raspberry Pi Zero 2W Pinout](https://github.com/user-attachments/assets/946e4078-6b62-4b7a-97ff-bac6b208822a)
> *Description: Pinout reference for Raspberry Pi Zero 2 WH.*


---



### 🔄 Adaptive Whitelist Feature Expansion
* **Core Technology**: Continuous Learning.
* **Operational Mechanism**: Extracts features from daily high-confidence recognition results and dynamically expands them into the local authorized whitelist database.
* **System Advantage**: The system can steadily optimize the efficiency of the recognition algorithm and overall user experience over time and daily use.

---

## 🏗️ System Architecture

**Client-Server Architecture**, separating lightweight control from heavy computation:

### 📡 Edge Node 
Deployed at the door
*   **Image Capture**: Captures real-time video through the camera.
*   **Low-Latency Transmission**: Uses TCP protocol to stream video to the indoor computing center.
*   **Physical Control**: Receives verification pass commands and drives the stepper motor to complete the physical door-opening action of "pushing back".

### 💻 Core Computing Node 
Deployed indoors
1.  **Gesture Wake-up**: Initiates the recognition process upon detecting a specific gesture.
2.  **Feature Locking & Enhancement**: Wakes up MediaPipe to lock facial features and immediately performs image enhancement (CLAHE) to overcome light interference.
3.  **Dual Recognition ( ArcFace + Facenet )**: First uses ArcFace for fast, high-precision determination; if edge values are encountered, seamlessly activates Facenet for secondary confirmation.


## 📂 Project Structure

```text
📦 Smart-Face-Lock
 ┣ 📂 pc_node/                 # PC Node: Core computing and AI recognition
 ┃ ┣ 📂 owners/                # Stores whitelist face photos ( needs to be created manually )
 ┃ ┣ 📂 intruders/             # Stores captured photos of intercepted strangers ( auto-generated )
 ┃ ┣ 📜 pc_gesture.py          # PC main program ( Gesture wake-up + Face recognition )
 ┃ ┗ 📜 requirements.txt       # PC node dependency list
 ┣ 📂 pi_node/                 # Raspberry Pi Node: Edge terminal and motor control
 ┃ ┣ 📜 pi_motor_server.py     # Receives door open commands and motor driver
 ┃ ┗ 📜 pi_stream_client.py    # Image capture and TCP stream push
 ┣ 📂 AWS/                     # Deployment scripts and automation tools
 ┣ 📜 .env.example             # Environment variables example file
 ┗ 📜 README.md
```
---

## 🛡️ Security & Cloud Integration

Security Mechanisms:

| Defense Mechanism | Operational Description |
| :--- | :--- |
| **🚨 Stranger Interception & Capture** | When a non-whitelist face is recognized, the system immediately refuses to open the door and automatically takes a photo of the scene. |
| **☁️ Real-time Cloud Upload** | By integrating the **Supabase** service, images and access logs are pushed to the cloud in real-time, facilitating remote monitoring. |
| **💾 Offline Cache Mechanism** | In response to network instability in real scenarios, a built-in **SQLite** local backup is provided. Security records are not lost during network disconnection, and will automatically retransmit once the network is restored. |

---

## ⚙️ Environment & Hardware Setup

### 【PC Node】 
* **Network Settings**: Default IP is `192.168.0.148`, must be on the same local area network ( LAN ) as the Raspberry Pi.
* **Software Dependencies**: Ensure required Python packages are installed, including OpenCV, mediapipe, deepface, and supabase.
* **Environment Setup**: Confirm that the cloud Supabase project environment and keys are configured.
* **Permission Directory**: Need to create an `owners/` folder in the project and place clear frontal face photos of authorized personnel as the whitelist.

### 【Raspberry Pi Node】
* **Network Settings**: Default IP is `192.168.0.192`.
* **Hardware Connection**: WebCam must be properly connected to the Pi's USB port.
* **Mechanism Control**: The stepper motor ( including ULN2003 driver board ) pins need to be connected to GPIO 17, 18, 27, 22. The system is designed so the motor **pushes the door open** upon receiving the command.

---

## 🚀 System Deployment & Startup

### Step 1: Sync Code to Edge Node
If scripts for the Pi are modified on the PC, go to the `AWS/` folder and run `upload_all_to_pi.bat`. The system will automatically upload files via SCP. Then run `ssh_to_pi.bat` to log into the Raspberry Pi terminal.

### Step 2: Sequential System Startup 
To ensure normal TCP Socket communication, follow this sequence:

| Sequence | Executing Device | Terminal Command | Status Description |
| :---: | :--- | :--- | :--- |
| **1** | 🍓 Raspberry Pi | `python pi_motor_server.py` | Opens Port `65432`, waiting to receive door-opening commands from the PC |
| **2** | 💻 PC Node | `python pc_gesture.py` | Opens Port `65434` waiting for video, and actively connects to the Pi to control the motor |
| **3** | 🍓 Raspberry Pi | `python pi_stream_client.py` | *( Open second terminal )* Starts the camera and streams the video to the PC node |

---

## 🛠️ Maintenance & Testing

* **Standalone Physical Door Lock Test**: SSH into the Raspberry Pi, execute `python test_motor.py`, and observe if the motor properly pushes the door backward.
* **Add/Remove Permissions**: Simply add or delete face photos in the `owners/` folder on the PC node. The permissions will update the next time the system wakes up.
* **Check Intruder Logs**: Go to the `intruders/` folder on the PC node to view captured screenshots of all intruders who failed verification ( refused entry ).

---

## 📦 Bill of Materials 

| Component Name | Specification/Model | Notes |
| :--- | :--- | :--- |
| **Edge Computing Board** | Raspberry Pi Zero 2 WH | Lightweight terminal, handles video streaming and motor control |
| **Camera Lens** | Compatible WebCam or Pi Camera | Installed outside the door, captures faces and gestures |
| **Stepper Motor** | 5V Stepper Motor | Responsible for the physical action of pushing the door backward |
| **Motor Driver Board** | ULN2003 | Receives Zero 2 WH GPIO signals to drive the motor |
| **Power Supply** | Pi Zero 2 W Dedicated Power Supply | Provides stable power to the edge computing board |
| **Storage & Flashing** | SD Card + SD Card Reader | Used to flash Raspberry Pi OS and store terminal code |
| **Adapter Accessories** | Micro USB Adapter | Used for Zero 2 WH to connect peripherals ( like camera ) |
| **Adapter Accessories** | Micro HDMI Adapter | Used for Zero 2 WH to connect a monitor for initial setup |
| **Peripherals** | Jumper Wires (Dupont) | Used to connect GPIO pins and the driver board |

---

## 👥 Team Members


| Name | Student ID |
| :---: | :---: |
| 羅奕程 | M11451021 |
| 王建傑 | M11451009 |
| 吳宗韓 | M11451019 |
| Peeranut Wiwarrawornchai | M11451801 |
