import cv2
import time
import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from detector import ObjectDetector
from ocr      import TextReader
from speaker  import Speaker

class BlindAssistant:
    def __init__(self):
        print("\n🚀 Starting Blind Assistant...")
        print("=" * 40)

        # ── Initialize Modules ───────────────────────
        print("🔄 Loading Speaker...")
        self.speaker = Speaker()
        time.sleep(1)

        print("🔄 Loading Object Detector...")
        self.detector = ObjectDetector()

        print("🔄 Loading Text Reader...")
        self.reader = TextReader()

        # ── Camera ───────────────────────────────────
        print("🔄 Starting Camera...")
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not self.cap.isOpened():
            print("❌ Camera not found!")
            exit()

        print("✅ Camera ready!")

        # ── Timing ───────────────────────────────────
        self.last_danger_time  = 0
        self.last_warning_time = 0
        self.last_normal_time  = 0
        self.last_ocr_time     = 0

        # ── Intervals (shorter = more responsive) ────
        self.danger_interval  = 2    # 🔴 Every 2 sec
        self.warning_interval = 4    # 🟠 Every 4 sec
        self.normal_interval  = 6    # 🟡🟢 Every 6 sec
        self.ocr_interval     = 6    # 📖 Every 6 sec

        # ── State ────────────────────────────────────
        self.mode         = "detection"
        self.current_text = None
        self.paused       = False

        print("=" * 40)
        print("✅ Blind Assistant Ready!\n")
        print("📋 Controls:")
        print("  D → Detection mode")
        print("  T → Text reading mode")
        print("  S → Describe scene")
        print("  P → Pause / Resume")
        print("  Q → Quit")
        print("=" * 40)

        # ── Welcome ───────────────────────────────────
        self.speaker.speak_and_wait(
            "Blind assistant is ready. "
            "I will describe everything around you."
        )

    # ─────────────────────────────────────────────────
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("❌ Camera error!")
                break

            current_time = time.time()

            if self.paused:
                self.draw_paused(frame)
                cv2.imshow("Blind Assistant", frame)

            else:
                if self.mode == "detection":
                    frame = self.run_detection(
                        frame, current_time
                    )
                elif self.mode == "ocr":
                    frame = self.run_ocr(
                        frame, current_time
                    )

                frame = self.draw_ui(frame)
                cv2.imshow("Blind Assistant", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("\n👋 Goodbye!")
                self.speaker.speak_and_wait(
                    "Goodbye! Stay safe!"
                )
                break

            elif key == ord('d'):
                self.mode         = "detection"
                self.current_text = None
                self.paused       = False
                print("\n🔍 Detection Mode")
                self.speaker.speak_and_wait(
                    "Object detection mode activated"
                )

            elif key == ord('t'):
                self.mode   = "ocr"
                self.paused = False
                print("\n📖 Text Reading Mode")
                self.speaker.speak_and_wait(
                    "Text reading mode activated. "
                    "Point camera at text."
                )

            elif key == ord('s'):
                self.describe_scene(frame)

            elif key == ord('p'):
                self.paused = not self.paused
                status = "Paused" if self.paused \
                         else "Resumed"
                print(f"\n⏸️ {status}")
                self.speaker.speak_and_wait(status)

        self.cleanup()

    # ─────────────────────────────────────────────────
    def run_detection(self, frame, current_time):
        """
        Detect objects and speak results
        DANGER always speaks immediately
        """
        # Detect
        detections = self.detector.detect(frame)
        frame      = self.detector.draw(frame, detections)

        if detections:

            # Sort by danger level
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

            # ── 🔴 DANGER ────────────────────────────
            # ALWAYS speaks no matter what
            # No is_speaking check here!
            if danger_objs:
                if current_time - self.last_danger_time \
                        > self.danger_interval:

                    msgs = []
                    for det in danger_objs[:3]:
                        msg = (
                            f"{det['label']} "
                            f"very close "
                            f"{det['direction']}"
                        )
                        msgs.append(msg)
                        print(f"  🔴 DANGER: {msg}")

                    # Force speak urgently
                    self.speaker.speak_urgent(
                        ". ".join(msgs)
                    )
                    self.last_danger_time = current_time

            # ── 🟠 WARNING ───────────────────────────
            # Speaks only when not speaking
            if warning_objs:
                if current_time - self.last_warning_time \
                        > self.warning_interval:
                    if not self.speaker.is_speaking:

                        msgs = []
                        for det in warning_objs[:2]:
                            msg = (
                                f"Caution. "
                                f"{det['label']} "
                                f"{det['direction']}, "
                                f"{det['distance']} centimeters"
                            )
                            msgs.append(msg)
                            print(f"  🟠 WARNING: {msg}")

                        self.speaker.speak(
                            ". ".join(msgs)
                        )
                        self.last_warning_time = current_time

            # ── 🟡 NEAR ──────────────────────────────
            if near_objs:
                if current_time - self.last_normal_time \
                        > self.normal_interval:
                    if not self.speaker.is_speaking:

                        msgs = []
                        for det in near_objs[:2]:
                            msg = (
                                f"{det['label']} "
                                f"nearby "
                                f"{det['direction']}, "
                                f"{det['distance']} centimeters"
                            )
                            msgs.append(msg)
                            print(f"  🟡 NEAR: {msg}")

                        self.speaker.speak(
                            ". ".join(msgs)
                        )
                        self.last_normal_time = current_time

            # ── 🟢 FAR ───────────────────────────────
            elif far_objs:
                if current_time - self.last_normal_time \
                        > self.normal_interval:
                    if not self.speaker.is_speaking:

                        msgs = []
                        for det in far_objs[:2]:
                            msg = (
                                f"{det['label']} "
                                f"{det['direction']}"
                            )
                            msgs.append(msg)
                            print(f"  🟢 FAR: {msg}")

                        self.speaker.speak(
                            ". ".join(msgs)
                        )
                        self.last_normal_time = current_time

        else:
            # Nothing detected
            if current_time - self.last_normal_time \
                    > self.normal_interval * 2:
                if not self.speaker.is_speaking:
                    print("  👁️ Nothing detected")
                    self.speaker.speak(
                        "Nothing detected around you"
                    )
                    self.last_normal_time = current_time

        # Show object count
        cv2.putText(
            frame,
            f"Objects: {len(detections)}",
            (10, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (255, 255, 255), 2
        )

        # Show danger count if any
        danger_count = len([
            d for d in detections
            if d["danger"] == "DANGER"
        ])
        if danger_count > 0:
            cv2.putText(
                frame,
                f"⚠️ DANGER: {danger_count}",
                (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 0, 255), 2
            )

        return frame

    # ─────────────────────────────────────────────────
    def run_ocr(self, frame, current_time):
        """
        Text reading mode
        """
        if current_time - self.last_ocr_time \
                > self.ocr_interval:
            if not self.speaker.is_speaking:

                text = self.reader.read_text(frame)

                if text:
                    self.current_text = text
                    print(f"\n📖 Found: {text}")
                    self.speaker.speak_and_wait(
                        f"I can read: {text}"
                    )
                else:
                    print("  📖 No text found")
                    self.speaker.speak_and_wait(
                        "No clear text found. "
                        "Point camera closer to text."
                    )

                self.last_ocr_time = current_time

        frame = self.reader.draw_text_box(
            frame, self.current_text
        )
        return frame

    # ─────────────────────────────────────────────────
    def describe_scene(self, frame):
        """
        Full scene description
        Speaks everything it sees
        """
        print("\n📊 Describing scene...")

        # Announce
        self.speaker.speak_and_wait(
            "Let me describe the scene"
        )

        # Detect
        detections = self.detector.detect(frame)

        if not detections:
            self.speaker.speak_and_wait(
                "I don't see anything around you"
            )
            return

        # Count objects
        counts = {}
        for det in detections:
            label = det["label"]
            counts[label] = counts.get(label, 0) + 1

        # Build description
        parts = []
        for label, count in counts.items():
            if count > 1:
                parts.append(f"{count} {label}s")
            else:
                parts.append(f"a {label}")

        description = "I can see " + ", ".join(parts)
        print(f"  📊 {description}")
        self.speaker.speak_and_wait(description)

        # Closest object
        valid = [
            d for d in detections
            if d["distance"] is not None
        ]
        if valid:
            closest = min(
                valid,
                key=lambda x: x["distance"]
            )
            closest_msg = (
                f"Closest object is "
                f"{closest['label']} "
                f"{closest['direction']}, "
                f"{closest['distance']} centimeters away"
            )
            print(f"  📍 {closest_msg}")
            self.speaker.speak_and_wait(closest_msg)

        # Danger objects
        danger_objs = [
            d for d in detections
            if d["danger"] == "DANGER"
        ]
        if danger_objs:
            # Speak each danger object
            for det in danger_objs:
                danger_msg = (
                    f"Warning! "
                    f"{det['label']} is very close "
                    f"{det['direction']}!"
                )
                print(f"  ⚠️ {danger_msg}")
                self.speaker.speak_and_wait(danger_msg)

    # ─────────────────────────────────────────────────
    def draw_ui(self, frame):
        """
        Draw UI elements
        """
        h, w = frame.shape[:2]

        # Top bar
        cv2.rectangle(
            frame,
            (0, 0), (w, 50),
            (0, 0, 0), -1
        )

        color = (0, 255, 0) \
            if self.mode == "detection" \
            else (255, 165, 0)

        cv2.putText(
            frame,
            f"MODE: {self.mode.upper()}",
            (10, 33),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9, color, 2
        )

        cv2.putText(
            frame,
            "D:Detect | T:Text | S:Scene | P:Pause | Q:Quit",
            (10, 48),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35, (180, 180, 180), 1
        )

        # Bottom bar
        cv2.rectangle(
            frame,
            (0, h - 40), (w, h),
            (0, 0, 0), -1
        )

        if self.speaker.is_speaking:
            status = "🔊 Speaking..."
            color  = (0, 255, 0)
        else:
            status = "✅ Ready"
            color  = (150, 150, 150)

        cv2.putText(
            frame, status,
            (10, h - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, color, 2
        )

        return frame

    # ─────────────────────────────────────────────────
    def draw_paused(self, frame):
        """
        Paused overlay
        """
        overlay = frame.copy()
        cv2.rectangle(
            overlay,
            (0, 0),
            (frame.shape[1], frame.shape[0]),
            (0, 0, 0), -1
        )
        cv2.addWeighted(
            overlay, 0.6,
            frame, 0.4,
            0, frame
        )
        cv2.putText(
            frame, "PAUSED",
            (frame.shape[1]//2 - 90,
             frame.shape[0]//2),
            cv2.FONT_HERSHEY_SIMPLEX,
            2, (255, 255, 255), 3
        )
        cv2.putText(
            frame, "Press P to resume",
            (frame.shape[1]//2 - 110,
             frame.shape[0]//2 + 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (200, 200, 200), 2
        )

    # ─────────────────────────────────────────────────
    def cleanup(self):
        """
        Release resources
        """
        self.speaker.stop()
        self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Cleanup done!")
        print("👋 Blind Assistant closed!")


# ── Run ──────────────────────────────────────────────────
if __name__ == "__main__":
    assistant = BlindAssistant()
    assistant.run()