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
  - [🧠 I. Edge-Side Biometric Intelligence](#-i-edge-side-biometric-intelligence)
  - [☁️ II. Cloud-Collaborative Security & Fault Tolerance](#️-ii-cloud-collaborative-security--fault-tolerance)
  - [📊 Architectural & Security Matrix](#-architectural--security-matrix)
- [🎥 Demo](#-demo)
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
> This framework proposes a hybrid edge-cloud architecture that aims to balance computational efficiency with robust access control. The proposed system is structurally divided into two primary domains: **Edge-Side Biometric Intelligence** and **Cloud-Collaborative Security**.

<br>

### 🧠 I. Edge-Side Biometric Intelligence

**🖐️ 1. Vision-Driven Low-Power Wake-Up Mechanism**
> - **Core Technology:** Lightweight Edge-based Gesture Detection Model.
> - **Operational Mechanism:** The device is designed to inherently maintain a low-power idle state. Upon the visual detection of a predefined hand gesture (e.g., raised index finger), the model initiates a transition to an active system wake-up state.
> - **System Advantage:** Has the potential to significantly improve edge energy efficiency by primarily allocating intensive computing resources during active recognition phases.

**👁️ 2. Dual-Engine Deep Learning Facial Recognition**
> - **Core Technology:** ArcFace & FaceNet dual-path verification, CLAHE dynamic image enhancement.
> - **Operational Mechanism:** Employs Contrast Limited Adaptive Histogram Equalization (CLAHE) to help mitigate the effects of variable or extreme lighting conditions prior to feature extraction. Subsequently, a dual-path algorithmic approach is utilized for cross-verification.
> - **System Advantage:** Aims to establish a resilient biometric perimeter, which may contribute to higher matching accuracy even in sub-optimal environmental conditions.

**🔄 3. Adaptive Whitelist Feature Expansion**
> - **Core Technology:** Continuous Edge-based Learning.
> - **Operational Mechanism:** Designed to dynamically extract latent features from high-confidence recognition instances, facilitating iterative updates to the local authorized whitelist database.
> - **System Advantage:** Intended to progressively refine algorithmic accuracy and potentially enhance the overall user experience (UX) through continuous operational learning.

---

### ☁️ II. Cloud-Collaborative Security & Fault Tolerance

**🚨 1. Near Real-Time Threat Interception & Cloud Synchronization**
> - **Core Technology:** Supabase Cloud Infrastructure.
> - **Operational Mechanism:** Upon the detection of an unauthorized or unverified facial profile, the system is programmed to deny entry and execute site image capture. The corresponding event logs and image payloads are subsequently transmitted to the Supabase cloud layer with minimal delay.
> - **System Advantage:** Facilitates a comprehensive access control audit trail and supports near real-time, remote monitoring capabilities.

**📶 2. Robust Asynchronous Fault-Tolerant Transmission**
> - **Core Technology:** SQLite Local Cache Layer & Background Asynchronous Threads.
> - **Operational Mechanism:** Functions as a distributed queue during network disruptions by caching captured media and access logs in a local SQLite database. Upon network restoration, asynchronous background threads are triggered to automatically execute payload retransmission.
> - **System Advantage:** Helps mitigate the risk of data loss during IoT network partitions, thereby contributing to a higher degree of audit log integrity.

<br>

### 📊 Architectural & Security Matrix

| Functional Module | Core Technology | Operational Paradigm | Key Benefit & Design Focus |
| :--- | :--- | :--- | :--- |
| **Standby & Wake-Up** | Lightweight Edge Gesture Model | Vision-Driven Activation | **Green Computing:** Tends to extend device operational lifespan. |
| **Biometric Verification** | ArcFace + FaceNet + CLAHE | Dual-Path Cross-Verification | **Fault Tolerance:** Helps mitigate lighting interference. |
| **Continuous Learning** | Adaptive Whitelist Algorithms | Dynamic Feature Expansion | **UX Optimization:** Designed to progressively improve recognition efficiency. |
| **Threat Management** | Supabase Cloud Integration | Near Real-Time Interception | **Security Auditing:** Supports low-latency remote monitoring. |
| **Network Resiliency** | SQLite + Async Threads | Offline Caching & Auto-Resume | **Data Integrity:** Aims to minimize the loss of security records. |

---

---


## 🎥 System Demonstration

> **Overview**  
> This section presents a comparative visual analysis of the operational outcomes between the **PC Core Computing Node** and the **Raspberry Pi Edge Node**. The demonstration aims to illustrate the practical execution and responsiveness of the proposed framework.

### 💻 1. PC Node

| 🚪 Physical Actuation Mechanism | 📡 Near Real-Time Video Stream Monitoring |
| :---: | :---: |
| <img src="docs/images/motor_action.gif" width="400" alt="Motor action gif"> | <img src="https://github.com/user-attachments/assets/9c8f5fee-e40e-4ea5-92ef-6c38fdc23ed2" width="400" alt="PC displays Raspberry Pi camera feed"> |
| *Upon successful biometric verification, a control signal is transmitted to actuate the motor, facilitating the physical opening of the door.* | *The PC node is designed to receive and render the TCP-based video stream transmitted from the external Raspberry Pi, enabling near real-time surveillance.* |
| ✅ **Verification Successful** | ❌ **Unauthorized Interception** |
| <img src="https://github.com/user-attachments/assets/80b85d77-0145-4645-b077-9794b14251f1" width="400" alt="Successfully recognized as owner"> | <img src="https://github.com/user-attachments/assets/1c32897d-4bc3-4983-9333-9518247a86f4" width="400" alt="Successfully recognized as non-owner"> |
| *Facial features are identified with a sufficient confidence threshold; the system subsequently displays a green visual indicator and initiates the access sequence.* | *Upon detecting a facial profile absent from the authorized whitelist, the system is programmed to deny access, triggering on-site image capture and cloud synchronization.* |

### 📡 2. Raspberry Pi Edge Node

**🍓 Hardware Configuration and Actuation Mechanism of the Edge Node**  
<br>
<img src="docs/images/pi_hardware_setup.jpg" width="800" alt="Hardware integration of Raspberry Pi">  
> *(Illustration of the physical integration comprising the Pi Zero 2 WH, camera module, stepper motor, and ULN2003 driver board)*

<br>

| 🔌 Motor Actuation Signal Reception | 👁️ TCP Connection and Stream Monitoring |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/126b227b-0d46-4c87-b6c6-c0394cf4d281" width="400" alt="Receiving signal from motor"> | <img src="https://github.com/user-attachments/assets/8bf7d43e-f972-43d8-9358-dd8468756bba" width="400" alt="Listening to return signal"> |
| *Terminal Output: Indicates the reception of the actuation command from the PC core node, preceding the initiation of GPIO control sequences.* | *Terminal Output: Demonstrates the establishment of the TCP connection, which is designed to facilitate ongoing video streaming and monitor bidirectional signaling.* |

---

### 🇬🇧 英文版 (English Version)

### ☁️ 3. Supabase Cloud Storage & Database

**📊 Unauthorized Access Logs and Image Repositories**  
<br>

| 📝 Unauthorized Access Event Logs | 📸 Captured Images of Unverified Subjects |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/0abd451e-686f-4d92-b985-6efd1f8c2240" width="400" alt="Supabase Log messages"> | <img src="https://github.com/user-attachments/assets/e38e38ea-110d-40ca-bb12-a2bdaba77342" width="400" alt="Supabase Intruder Photos"> |
| *Supabase Database: Maintains detailed logs outlining the temporal data and associated states of unauthorized access attempts.* | *Supabase Storage: Designed to automatically capture and upload image frames of unrecognized subjects to the cloud repository.* |

---

## 🗺️ Architectural Diagrams

### 1. System Workflow and Data Pipeline
![System Flowchart](https://github.com/user-attachments/assets/dc2e7bb6-07af-4c1f-b153-2d094064efb9)
> *Description: Illustrates the proposed operational lifecycle, spanning from gesture-based activation and dynamic image enhancement, through the dual-model (ArcFace + FaceNet) biometric verification process, to the execution of physical actuation and subsequent cloud synchronization.*

### 2. Hardware Interconnection Diagram 
![Wiring Diagram between Raspberry Pi and Motor](https://github.com/user-attachments/assets/267edc6a-3bf9-47bf-87c8-c79290d8395a)
> *Description: Depicts the specific GPIO wiring configuration bridging the Raspberry Pi Zero 2 WH and the ULN2003 stepper motor driver module.*

### 3. Raspberry Pi Zero 2W Pinout Reference
![Raspberry Pi Zero 2W Pinout](https://github.com/user-attachments/assets/946e4078-6b62-4b7a-97ff-bac6b208822a)
> *Description: Provides the standard GPIO pinout reference for the Raspberry Pi Zero 2 WH utilized within this framework.*


---

## 📂 Repository Structure

```text
📦 Smart-Face-Lock
 ┣ 📂 pc_node/                 # PC Node: Core computational hub for AI-driven recognition tasks
 ┃ ┣ 📂 owners/                # Repository for authorized whitelist biometric templates (requires manual initialization)
 ┃ ┣ 📂 intruders/             # Local cache for captured images of unverified subjects (automatically populated)
 ┃ ┣ 📜 pc_gesture.py          # Primary execution script (integrates gesture activation and biometric verification)
 ┃ ┗ 📜 requirements.txt       # Dependency specifications for the PC environment
 ┣ 📂 pi_node/                 # Edge Node: Handles media capture and motor actuation
 ┃ ┣ 📜 pi_motor_server.py     # Server script designed to receive actuation signals and drive the motor
 ┃ ┗ 📜 pi_stream_client.py    # Client script for continuous image capture and TCP-based stream transmission
 ┣ 📂 AWS/                     # Infrastructure deployment scripts and automation configurations
 ┣ 📜 .env.example             # Template for defining system environment variables
 ┗ 📜 README.md
```
---

## 🏗️ System Architecture

**Distributed Client-Server Framework**, designed to decouple lightweight edge-based actuation from computationally intensive tasks:

### 📡 Edge Node 
*Deployed at the access point*
*   **Image Acquisition**: Facilitates real-time video capture via the integrated camera module.
*   **Low-Latency Transmission**: Utilizes the TCP protocol to stream video payloads to the central computing node with minimal delay.
*   **Physical Actuation**: Designed to receive verification-success signals and drive the stepper motor, facilitating the mechanical unlocking sequence.

### 💻 Core Computing Node 
*Deployed in a secure indoor environment*
1.  **Gesture-Triggered Activation**: Initiates the biometric recognition sequence upon the detection of predefined hand gestures.
2.  **Feature Localization & Enhancement**: Invokes MediaPipe to identify facial landmarks and subsequently applies Contrast Limited Adaptive Histogram Equalization (CLAHE) to help mitigate variable lighting interference.
3.  **Dual-Path Biometric Verification (ArcFace + FaceNet)**: Primarily utilizes ArcFace for high-efficiency assessment; in cases of marginal confidence scores, the system is engineered to dynamically invoke FaceNet for secondary cross-verification.

---

## ⚙️ Environment & Hardware Setup

### 【PC Node】 
* **Network Configuration**: The default IP address is `192.168.0.148`; it is required to be deployed within the same Local Area Network (LAN) as the edge node.
* **Software Dependencies**: Necessitates the installation of specific Python libraries, including OpenCV, MediaPipe, DeepFace, and Supabase.
* **Environment Initialization**: Requires proper configuration of the Supabase cloud project parameters and associated API keys.
* **Access Control Directory**: Requires the creation of an `owners/` directory within the project, populated with clear, frontal facial images to serve as the authorized biometric whitelist.

### 【Raspberry Pi Node】
* **Network Configuration**: The default IP address is `192.168.0.192`.
* **Hardware Interface**: The camera module must be securely interfaced with the Raspberry Pi via the USB port.
* **Actuation Control**: The stepper motor (alongside the ULN2003 driver board) must be connected to GPIO pins 17, 18, 27, and 22. The system is configured such that the motor actuates the unlocking mechanism upon command reception.

---

## 🚀 System Deployment & Initialization

### Step 1: Code Synchronization to Edge Node
To propagate script modifications from the PC to the Raspberry Pi, execute `upload_all_to_pi.bat` located in the `AWS/` directory to automate SCP file transfers. Subsequently, utilize `ssh_to_pi.bat` to establish a secure terminal session with the edge node.

### Step 2: Sequential System Initialization 
To establish stable TCP Socket communication, the following initialization sequence is recommended:

| Sequence | Executing Device | Terminal Command | Status Description |
| :---: | :--- | :--- | :--- |
| **1** | 🍓 Raspberry Pi | `python pi_motor_server.py` | Initializes Port `65432`, awaiting actuation commands from the core node. |
| **2** | 💻 PC Node | `python pc_gesture.py` | Initializes Port `65434` for video reception and actively establishes a connection for motor control. |
| **3** | 🍓 Raspberry Pi | `python pi_stream_client.py` | *(Secondary terminal)* Initiates the camera module and streams video data to the PC node. |

---

## 🛠️ Maintenance & Testing

* **Standalone Actuation Test**: Establish an SSH connection to the edge node and execute `test_motor.py` to verify whether the motor correctly executes the mechanical unlocking sequence.
* **Access Privilege Management**: Modifications to access rights can be managed by adding or removing facial templates in the PC node's `owners/` directory. These changes are typically processed during the subsequent system activation cycle.
* **Audit of Unverified Access Attempts**: Navigate to the `intruders/` directory on the PC node to review locally cached images of subjects who failed the biometric verification protocols.

---

## 📦 Bill of Materials 

| Component Name | Specification / Model | Functional Description |
| :--- | :--- | :--- |
| **Edge Computing Board** | Raspberry Pi Zero 2 WH | Lightweight edge terminal; processes video streaming and motor actuation. |
| **Optical Sensor** | Compatible WebCam / Pi Camera | Deployed at the access point for facial and gesture data acquisition. |
| **Actuator** | 5V Stepper Motor | Mechanical component responsible for executing the unlocking mechanism. |
| **Motor Driver** | ULN2003 | Receives GPIO control signals from the edge board to drive the actuator. |
| **Power Supply Unit** | Pi Zero 2 W Dedicated PSU | Delivers stable electrical power to the edge computing hardware. |
| **Storage Media** | MicroSD Card + Reader | Utilized for OS deployment and local script storage. |
| **Interface Adapter** | Micro USB to USB-A Adapter | Facilitates the connection of external peripherals (e.g., optical sensor). |
| **Display Adapter** | Micro HDMI Adapter | Enables monitor connectivity for initial system configuration. |
| **Interconnects** | Jumper Wires (Dupont) | Establishes electrical connections between GPIO pins and the driver board. |

---

## 👥 Team Members


| Name | Student ID |
| :---: | :---: |
| 羅奕程 | M11451021 |
| 王建傑 | M11451009 |
| 吳宗韓 | M11451019 |
| Peeranut Wiwarrawornchai | M11451801 |
