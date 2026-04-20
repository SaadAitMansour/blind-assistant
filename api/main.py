import cv2
import sys
import os
import time
import base64
import asyncio
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket
import uvicorn

# Add modules to path
sys.path.append(
    os.path.join(os.path.dirname(__file__), '../modules')
)

from detector import ObjectDetector
from ocr      import TextReader
from speaker  import Speaker

# ── App Setup ────────────────────────────────────────────
app = FastAPI(
    title="Blind Assistant API",
    version="1.0.0"
)

# ── CORS ─────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global State ─────────────────────────────────────────
class AppState:
    def __init__(self):
        self.detector    = None
        self.reader      = None
        self.speaker     = None
        self.cap         = None
        self.mode        = "detection"
        self.running     = False
        self.detections  = []
        self.current_text = None

        # Timing
        self.last_danger_time  = 0
        self.last_warning_time = 0
        self.last_normal_time  = 0
        self.last_ocr_time     = 0

        # Intervals
        self.danger_interval  = 3
        self.warning_interval = 5
        self.normal_interval  = 7
        self.ocr_interval     = 6

state = AppState()

# ── Startup ───────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    print("🔄 Loading modules...")

    state.speaker  = Speaker()
    time.sleep(1)
    state.detector = ObjectDetector()
    state.reader   = TextReader()

    # Start camera
    state.cap = cv2.VideoCapture(0)
    state.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    state.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    state.running = True
    print("✅ All modules loaded!")

    state.speaker.speak_and_wait(
        "Blind assistant web interface is ready"
    )

# ── Shutdown ──────────────────────────────────────────────
@app.on_event("shutdown")
async def shutdown():
    state.running = False
    if state.cap:
        state.cap.release()
    if state.speaker:
        state.speaker.stop()
    print("✅ Shutdown complete!")

# ── Helper: Frame to Base64 ───────────────────────────────
def frame_to_base64(frame):
    """
    Convert OpenCV frame to base64
    So we can send it to browser
    """
    _, buffer = cv2.imencode('.jpg', frame, 
        [cv2.IMWRITE_JPEG_QUALITY, 80])
    b64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{b64}"

# ── Helper: Process Frame ─────────────────────────────────
def process_frame(frame):
    """
    Process frame based on current mode
    Returns processed frame + data
    """
    current_time = time.time()
    data = {
        "mode":       state.mode,
        "detections": [],
        "text":       None,
        "speaking":   state.speaker.is_speaking
    }

    if state.mode == "detection":
        # Detect objects
        detections = state.detector.detect(frame)
        frame      = state.detector.draw(frame, detections)

        # Update state
        state.detections = detections

        # Build detection data
        data["detections"] = [
            {
                "label":     d["label"],
                "distance":  d["distance"],
                "direction": d["direction"],
                "danger":    d["danger"],
            }
            for d in detections
        ]

        # Speak based on danger
        if detections:
            danger_objs  = [
                d for d in detections
                if d["danger"] == "DANGER"
            ]
            warning_objs = [
                d for d in detections
                if d["danger"] == "WARNING"
            ]
            near_objs    = [
                d for d in detections
                if d["danger"] == "NEAR"
            ]
            far_objs     = [
                d for d in detections
                if d["danger"] == "FAR"
            ]

            # 🔴 DANGER
            if danger_objs:
                if current_time - state.last_danger_time \
                        > state.danger_interval:
                    if not state.speaker.is_speaking:
                        msgs = []
                        for det in danger_objs[:2]:
                            msgs.append(
                                f"{det['label']} very close "
                                f"{det['direction']}"
                            )
                        state.speaker.speak_urgent(
                            ". ".join(msgs)
                        )
                        state.last_danger_time = current_time

            # 🟠 WARNING
            if warning_objs:
                if current_time - state.last_warning_time \
                        > state.warning_interval:
                    if not state.speaker.is_speaking:
                        msgs = []
                        for det in warning_objs[:2]:
                            msgs.append(
                                f"Caution. {det['label']} "
                                f"{det['direction']}, "
                                f"{det['distance']} centimeters"
                            )
                        state.speaker.speak(". ".join(msgs))
                        state.last_warning_time = current_time

            # 🟡 NEAR
            if near_objs:
                if current_time - state.last_normal_time \
                        > state.normal_interval:
                    if not state.speaker.is_speaking:
                        msgs = []
                        for det in near_objs[:2]:
                            msgs.append(
                                f"{det['label']} nearby "
                                f"{det['direction']}, "
                                f"{det['distance']} centimeters"
                            )
                        state.speaker.speak(". ".join(msgs))
                        state.last_normal_time = current_time

            # 🟢 FAR
            elif far_objs:
                if current_time - state.last_normal_time \
                        > state.normal_interval:
                    if not state.speaker.is_speaking:
                        msgs = []
                        for det in far_objs[:2]:
                            msgs.append(
                                f"{det['label']} "
                                f"{det['direction']}"
                            )
                        state.speaker.speak(". ".join(msgs))
                        state.last_normal_time = current_time

        else:
            if current_time - state.last_normal_time \
                    > state.normal_interval * 2:
                if not state.speaker.is_speaking:
                    state.speaker.speak(
                        "Nothing detected around you"
                    )
                    state.last_normal_time = current_time

    elif state.mode == "ocr":
        if current_time - state.last_ocr_time \
                > state.ocr_interval:
            if not state.speaker.is_speaking:
                text = state.reader.read_text(frame)
                if text:
                    state.current_text = text
                    state.speaker.speak_and_wait(
                        f"I can read: {text}"
                    )
                else:
                    state.speaker.speak_and_wait(
                        "No clear text found."
                    )
                state.last_ocr_time = current_time

        data["text"] = state.current_text
        frame = state.reader.draw_text_box(
            frame, state.current_text
        )

    return frame, data

# ── REST Endpoints ────────────────────────────────────────
@app.get("/")
def root():
    return {
        "message": "Blind Assistant API Running 🚀",
        "mode":    state.mode
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/mode/{new_mode}")
def set_mode(new_mode: str):
    """
    Switch between detection and ocr mode
    """
    if new_mode not in ["detection", "ocr"]:
        return {"error": "Invalid mode"}

    state.mode         = new_mode
    state.current_text = None
    print(f"\n🔄 Mode: {new_mode}")

    state.speaker.speak_and_wait(
        f"{new_mode} mode activated"
    )

    return {"mode": state.mode}

@app.post("/scene")
def describe_scene():
    """
    Describe current scene
    """
    if not state.cap:
        return {"error": "Camera not ready"}

    ret, frame = state.cap.read()
    if not ret:
        return {"error": "Camera error"}

    detections = state.detector.detect(frame)

    if not detections:
        state.speaker.speak_and_wait(
            "I don't see anything around you"
        )
        return {"description": "Nothing detected"}

    # Count objects
    counts = {}
    for det in detections:
        label = det["label"]
        counts[label] = counts.get(label, 0) + 1

    parts = []
    for label, count in counts.items():
        if count > 1:
            parts.append(f"{count} {label}s")
        else:
            parts.append(f"a {label}")

    description = "I can see " + ", ".join(parts)
    state.speaker.speak_and_wait(description)

    # Closest object
    valid = [
        d for d in detections
        if d["distance"] is not None
    ]
    closest_msg = None
    if valid:
        closest = min(valid, key=lambda x: x["distance"])
        closest_msg = (
            f"Closest is {closest['label']} "
            f"{closest['direction']}, "
            f"{closest['distance']} centimeters"
        )
        state.speaker.speak_and_wait(closest_msg)

    return {
        "description": description,
        "closest":     closest_msg,
        "count":       len(detections)
    }

@app.get("/status")
def get_status():
    return {
        "mode":      state.mode,
        "speaking":  state.speaker.is_speaking
            if state.speaker else False,
        "detections": len(state.detections),
        "running":   state.running
    }

# ── WebSocket ─────────────────────────────────────────────
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket for live camera feed
    Sends frames + detection data
    to frontend in real time
    """
    await websocket.accept()
    print("✅ WebSocket connected!")

    try:
        while state.running:
            # Read frame
            ret, frame = state.cap.read()
            if not ret:
                break

            # Process frame in thread
            loop = asyncio.get_event_loop()
            frame, data = await loop.run_in_executor(
                None, process_frame, frame
            )

            # Convert to base64
            img_b64 = frame_to_base64(frame)

            # Send to frontend
            await websocket.send_json({
                "image":      img_b64,
                "data":       data,
            })

            # Small delay
            await asyncio.sleep(0.033)  # ~30 FPS

    except Exception as e:
        print(f"❌ WebSocket error: {e}")
    finally:
        print("❌ WebSocket disconnected!")

# ── Run ──────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )