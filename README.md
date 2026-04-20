# 👁️ Blind Assistant AI

Real-time AI assistant for visually impaired people.
Uses computer vision to detect objects, read text,
and provide voice guidance.

## Features
- 🔍 Real-time object detection
- 📏 Distance estimation
- 🗺️ Direction detection
- 📖 Text reading (OCR)
- 🔊 Voice output
- 🌐 Web interface

## Tech Stack
- Python + OpenCV
- YOLOv8
- Tesseract OCR
- FastAPI + WebSockets
- React + Tailwind CSS

## Setup

### AI Pipeline & Backend
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install opencv-python
pip install ultralytics
pip install pytesseract
pip install pyttsx3
pip install fastapi
pip install uvicorn
pip install websockets

# Download YOLO model
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"