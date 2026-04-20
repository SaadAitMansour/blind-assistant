import cv2
import sys
import os
from ultralytics import YOLO

# Add modules to path
sys.path.append(os.path.dirname(__file__))
from distance import DistanceEstimator

class ObjectDetector:
    def __init__(self):
        print("🔄 Loading YOLO model...")
        self.model = YOLO('yolov8n.pt')
        self.distance_estimator = DistanceEstimator()

        # Confidence threshold
        self.confidence = 0.5

        # Box colors based on danger
        self.colors = {
            "DANGER":  (0, 0, 255),    # Red
            "WARNING": (0, 165, 255),  # Orange
            "NEAR":    (0, 255, 255),  # Yellow
            "FAR":     (0, 255, 0),    # Green
        }

        print("✅ YOLO model loaded!")

    def detect(self, frame):
        """
        Detect all objects in frame
        Returns list of detections
        """
        results = self.model(
            frame,
            conf=self.confidence,
            verbose=False
        )

        detections = []

        for result in results:
            boxes = result.boxes
            for box in boxes:

                # Get details
                label       = self.model.names[int(box.cls)]
                confidence  = float(box.conf)
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Calculate dimensions
                bbox_height   = y2 - y1
                bbox_center_x = (x1 + x2) // 2
                frame_width   = frame.shape[1]

                # Estimate distance
                distance, danger = self.distance_estimator.estimate(
                    label, bbox_height
                )

                # Get direction
                direction = self.distance_estimator.get_direction(
                    frame_width, bbox_center_x
                )

                detections.append({
                    "label":      label,
                    "confidence": round(confidence, 2),
                    "distance":   distance,
                    "danger":     danger,
                    "direction":  direction,
                    "bbox":       (x1, y1, x2, y2)
                })

        return detections

    def draw(self, frame, detections):
        """
        Draw boxes and labels on frame
        """
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            danger   = det["danger"]
            label    = det["label"]
            distance = det["distance"]
            direction = det["direction"]

            # Get color
            color = self.colors.get(danger, (0, 255, 0))

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1), (x2, y2),
                color, 2
            )

            # Draw background for text
            text = f"{label} {distance}cm"
            (tw, th), _ = cv2.getTextSize(
                text,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, 2
            )
            cv2.rectangle(
                frame,
                (x1, y1 - th - 10),
                (x1 + tw, y1),
                color, -1
            )

            # Draw label text
            cv2.putText(
                frame, text,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 0, 0), 2
            )

            # Draw danger level
            cv2.putText(
                frame, danger,
                (x1, y2 + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, color, 2
            )

        return frame


# ── Test ─────────────────────────────────────────────────
if __name__ == "__main__":
    detector = ObjectDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not found!")
        exit()

    print("\n📷 Camera started!")
    print("─" * 40)
    print("  Q → Quit")
    print("─" * 40)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera error!")
            break

        # Detect objects
        detections = detector.detect(frame)

        # Draw on frame
        frame = detector.draw(frame, detections)

        # Print detections
        if detections:
            print("\n🔍 Detected:")
            for det in detections:
                print(f"  → {det['label']:15} | "
                      f"{str(det['distance'])+'cm':8} | "
                      f"{det['danger']:7} | "
                      f"{det['direction']}")

        # Show FPS
        cv2.putText(
            frame,
            f"Objects: {len(detections)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (255, 255, 255), 2
        )

        cv2.imshow("Detector Test 🔍", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Detector test done!")