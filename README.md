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

- [🛠️ Technical Architecture](#️-technical-architecture)
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
- [📂 Project Structure](#-project-structure)
- [🏗️ System Architecture](#️-system-architecture)
  - [📡 Edge Node](#-edge-node)
  - [💻 Core Computing Node](#-core-computing-node)
- [🛡️ Security & Cloud Integration](#️-security--cloud-integration)
- [⚙️ Environment & Hardware Setup](#️-environment--hardware-setup)
  - [【PC Node】](#pc-node)
  - [【Raspberry Pi Node】](#raspberry-pi-node)
- [🚀 System Deployment & Startup](#-system-deployment--startup)
  - [Step 1: Sync Code to Edge Node](#step-1-sync-code-to-edge-node)
  - [Step 2: Sequential System Startup](#step-2-sequential-system-startup)
- [🛠️ Maintenance & Testing](#️-maintenance--testing)
- [📦 Bill of Materials](#-bill-of-materials)
- [👥 Team Members](#-team-members)

</details>

## 🛠️ Technical Architecture

> **Overview** 
> This framework proposes a highly resilient, hybrid edge-cloud architecture designed to optimize computational efficiency while ensuring robust access control. The system is structurally divided into **Edge-Side Biometric Intelligence** and **Cloud-Collaborative Security**.

<br>

### 🧠 I. Edge-Side Biometric Intelligence

**🖐️ 1. Vision-Driven Ultra-Low-Power Wake-Up**
> - **Core Technology:** Lightweight Edge Gesture Detection Model.
> - **Operational Mechanism:** The device inherently maintains an ultra-low-power idling state. Upon the visual detection of a predefined hand gesture (e.g., raised index finger), the model triggers an instantaneous transition to a full-system wake-up.
> - **System Advantage:** Drastically optimizes edge energy efficiency by exclusively allocating intensive computing resources during active recognition phases.

**👁️ 2. Dual-Engine Deep Learning Facial Recognition**
> - **Core Technology:** ArcFace & FaceNet dual-track verification, CLAHE dynamic image enhancement.
> - **Operational Mechanism:** Implements Contrast Limited Adaptive Histogram Equalization (CLAHE) to mitigate extreme lighting conditions prior to feature extraction. Subsequently, it employs a dual-track algorithmic paradigm for cross-verification.
> - **System Advantage:** Establishes a highly resilient biometric perimeter, guaranteeing exceptional matching accuracy even in sub-optimal environments.

**🔄 3. Adaptive Whitelist Feature Expansion**
> - **Core Technology:** Continuous Edge Learning.
> - **Operational Mechanism:** Dynamically extracts latent features from daily high-confidence recognition instances, iteratively updating the local authorized whitelist database.
> - **System Advantage:** Progressively refines algorithmic accuracy and optimizes the user experience (UX) through daily operational learning.

---

### ☁️ II. Cloud-Collaborative Security & Fault Tolerance

**🚨 1. Zero-Latency Threat Interception & Cloud Synchronization**
> - **Core Technology:** Supabase Cloud Infrastructure.
> - **Operational Mechanism:** Upon interception of an unauthorized or unverified facial profile, the system instantly refuses entry and executes site capture. The event logs and image payloads are synchronously pushed to the Supabase cloud layer.
> - **System Advantage:** Facilitates a strict access control audit trail and enables sub-second, remote zero-latency monitoring.

**📶 2. Robust Asynchronous Fault-Tolerant Transmission**
> - **Core Technology:** SQLite Local Cache Layer & Background Asynchronous Threads.
> - **Operational Mechanism:** Simulates a distributed queue during network disruptions by caching captured media and access logs in a local SQLite database. Upon network restoration, asynchronous background threads automatically execute payload retransmission.
> - **System Advantage:** Effectively mitigates data loss during IoT network partitions, guaranteeing 100% audit log integrity.

<br>

### 📊 Architectural & Security Matrix

| Functional Module | Core Technology | Operational Paradigm | Key Benefit & Design Focus |
| :--- | :--- | :--- | :--- |
| **Standby & Wake-Up** | Lightweight Edge Gesture Model | Vision-Driven Activation | **Green Computing:** Drastically extends device longevity. |
| **Biometric Verification** | ArcFace + FaceNet + CLAHE | Dual-Track Cross-Verification | **High Fault Tolerance:** Overcomes extreme lighting interference. |
| **Continuous Learning** | Adaptive Whitelist Algorithms | Dynamic Feature Expansion | **UX Optimization:** Steadily improves recognition efficiency. |
| **Threat Management** | Supabase Cloud Integration | Real-time Interception & Push | **Zero-Latency Auditing:** Instantaneous remote monitoring. |
| **Network Resiliency** | SQLite + Async Threads | Offline Caching & Auto-Resume | **Data Integrity:** Guarantees zero loss of security records. |

---

## 🎥 Demo

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
