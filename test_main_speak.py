import sys
import os
import time
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from speaker  import Speaker
from detector import ObjectDetector

print("🔄 Loading modules...")
speaker  = Speaker()
detector = ObjectDetector()
time.sleep(1)

print("🔄 Starting camera...")
cap = cv2.VideoCapture(0)

# Timing
last_speak_time = 0
speak_interval  = 5   # Every 5 seconds

print("✅ Running... Press Q to quit")
print("─" * 40)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()

    # Detect
    detections = detector.detect(frame)

    # Show frame
    cv2.imshow("Debug Test", frame)

    # Only speak if:
    # 1. Enough time passed
    # 2. Not already speaking
    if current_time - last_speak_time > speak_interval:
        if not speaker.is_speaking:
            if detections:
                det = detections[0]
                msg = (
                    f"{det['label']} "
                    f"{det['direction']} "
                    f"{det['distance']} centimeters"
                )
                print(f"📤 Speaking: {msg}")
                speaker.speak(msg)
            else:
                print("📤 Nothing detected")
                speaker.speak("Nothing detected")

            last_speak_time = current_time

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
speaker.stop()