# 👁️ Blind Assistant AI

> Real-time AI assistant for visually impaired people.
> Uses computer vision to detect objects, read text,
> and provide voice guidance.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square)
![YOLOv8](https://img.shields.io/badge/YOLOv8-latest-green?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📋 Table of Contents
- [What It Does](#what-it-does)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Run](#run)
- [Controls](#controls)
- [Danger Levels](#danger-levels)
- [Author](#author)

---

## 🎯 What It Does

    📷 Camera captures real world
             ↓
    🔍 Detects objects around person
             ↓
    📏 Estimates distance & direction
             ↓
    📖 Reads any text it sees
             ↓
    🔊 Speaks everything out loud
             ↓
    ⚠️  Warns about dangers

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 Object Detection | Detects 80+ objects in real time |
| 📏 Distance Estimation | Measures how far objects are |
| 🗺️ Direction Detection | Left / Right / In front of you |
| 🚨 Danger Alerts | Warns when objects are too close |
| 📖 Text Reading | Reads signs, labels, books aloud |
| 🔊 Voice Output | Speaks everything in English |
| 🌐 Web Interface | Control via browser |
| ⏸️ Pause / Resume | Pause anytime |

---

## 🛠️ Tech Stack

| Part | Technology |
|------|-----------|
| Object Detection | YOLOv8 (Ultralytics) |
| OCR / Text Reading | Tesseract OCR |
| Voice Output | Windows SAPI (VBScript) |
| Image Processing | OpenCV |
| Backend API | FastAPI + WebSockets |
| Frontend | React + Tailwind CSS |
| Real-time Feed | WebSockets |

---

## 📁 Project Structure

    blind-assistant/
    │
    ├── 📁 modules/
    │   ├── speaker.py        → Voice output module
    │   ├── detector.py       → Object detection (YOLOv8)
    │   ├── ocr.py            → Text reading (Tesseract)
    │   └── distance.py       → Distance & direction estimation
    │
    ├── 📁 api/
    │   └── main.py           → FastAPI backend + WebSocket
    │
    ├── 📁 web/
    │   ├── src/
    │   │   ├── components/
    │   │   │   ├── Header.jsx
    │   │   │   ├── CameraFeed.jsx
    │   │   │   ├── Controls.jsx
    │   │   │   ├── DetectionList.jsx
    │   │   │   └── StatusBar.jsx
    │   │   ├── hooks/
    │   │   │   └── useWebSocket.js
    │   │   └── App.js
    │   └── package.json
    │
    ├── 📁 models/            → YOLO model (download separately)
    ├── 📁 known_faces/       → Add photos for face recognition
    │
    ├── 📄 main.py            → Desktop app entry point
    ├── 📄 requirements.txt   → Python dependencies
    ├── 📄 README.md          → This file
    └── 📄 .gitignore

---

## 🚀 Setup

### Prerequisites

    ✅ Python 3.8+
    ✅ Node.js 16+
    ✅ Webcam
    ✅ Windows OS (for voice output)
    ✅ Tesseract OCR installed

### 1. Clone Repository

    git clone https://github.com/SaadAitMansour/blind-assistant.git
    cd blind-assistant

### 2. Create Virtual Environment

    python -m venv venv
    venv\Scripts\activate

### 3. Install Python Dependencies

    pip install -r requirements.txt

### 4. Install Tesseract OCR

    1. Download installer from:
       https://github.com/UB-Mannheim/tesseract/wiki

    2. Install with default settings

    3. Default path:
       C:\Program Files\Tesseract-OCR\

    4. Download English language file:
       https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

    5. Place in:
       C:\Program Files\Tesseract-OCR\tessdata\

### 5. Download YOLO Model

    python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
    move yolov8n.pt models\

### 6. Install Frontend Dependencies

    cd web
    npm install
    cd ..

---

## ▶️ Run

### Option 1 - Desktop App

    venv\Scripts\activate
    python main.py

### Option 2 - Web Interface

    Terminal 1 - Backend:
    venv\Scripts\activate
    cd api
    python main.py

    Terminal 2 - Frontend:
    cd web
    npm start

    Open Browser → http://localhost:3000

---

## ⌨️ Desktop Controls

| Key | Action |
|-----|--------|
| D | Object detection mode |
| T | Text reading mode |
| S | Describe full scene |
| P | Pause / Resume |
| Q | Quit |

---

## 🌐 Web Controls

| Button | Action |
|--------|--------|
| 🔍 Detection | Switch to object detection |
| 📖 Text Reading | Switch to OCR mode |
| 📊 Describe Scene | Full scene description |
| ⏸️ Pause | Pause the assistant |
| ❌ Quit | Stop the assistant |

---

## 🎯 Danger Levels

| Level | Color | Distance | Action |
|-------|-------|----------|--------|
| DANGER | 🔴 Red | < 80cm | Immediate warning |
| WARNING | 🟠 Orange | < 150cm | Caution alert |
| NEAR | 🟡 Yellow | < 300cm | Nearby alert |
| FAR | 🟢 Green | > 300cm | Info only |

---

## ⚠️ Common Issues

| Issue | Fix |
|-------|-----|
| Camera not found | Check webcam connection |
| Tesseract error | Check installation path |
| No voice output | Check Windows voice settings |
| YOLO not found | Run download command above |
| Port in use | Change port in api/main.py |

---

## 🔮 Future Features

    📌 Face recognition
    📌 Currency detection
    📌 Color detection
    📌 Mobile app version
    📌 Arabic language support
    📌 GPS navigation

---

## 👥 Author

**Saad Ait Mansour**
- GitHub: [@SaadAitMansour](https://github.com/SaadAitMansour)

---

## 📄 License

This project is licensed under the
MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)