class DistanceEstimator:
    def __init__(self):
        # Average real world sizes (cm)
        self.real_sizes = {
            'person':        170,
            'car':           450,
            'truck':         600,
            'bus':           1000,
            'motorcycle':    200,
            'bicycle':       150,
            'chair':         80,
            'bottle':        25,
            'cup':           10,
            'laptop':        35,
            'phone':         15,
            'book':          25,
            'dog':           50,
            'cat':           30,
            'table':         75,
            'tv':            80,
            'door':          200,
            'traffic light': 100,
            'fire hydrant':  60,
            'stop sign':     90,
            'bench':         150,
            'default':       50
        }

        # Laptop webcam focal length
        self.focal_length = 615

    def estimate(self, label, bbox_height):
        """
        Estimate distance from camera
        Input  → label + bounding box height
        Output → distance in cm + danger level
        """
        if bbox_height == 0:
            return None, None

        # Get real size
        real_size = self.real_sizes.get(
            label.lower(),
            self.real_sizes['default']
        )

        # Calculate distance
        distance = (real_size * self.focal_length) / bbox_height

        # Get danger level
        danger = self.get_danger_level(distance)

        return round(distance), danger

    def get_danger_level(self, distance):
        """
        Classify distance into danger levels
        """
        if distance < 80:
            return "DANGER"      # Very close  🔴
        elif distance < 150:
            return "WARNING"     # Close       🟠
        elif distance < 300:
            return "NEAR"        # Nearby      🟡
        else:
            return "FAR"         # Safe        🟢

    def get_direction(self, frame_width, bbox_center_x):
        """
        Detect which direction object is
        """
        left_zone  = frame_width // 3
        right_zone = (frame_width // 3) * 2

        if bbox_center_x < left_zone:
            return "on your left"
        elif bbox_center_x > right_zone:
            return "on your right"
        else:
            return "in front of you"


# ── Test ─────────────────────────────────────────────────
if __name__ == "__main__":
    estimator = DistanceEstimator()

    # Test cases
    tests = [
        ("person", 400),   # Very close
        ("person", 200),   # Medium
        ("person", 100),   # Far
        ("car",    300),   # Car close
        ("bottle", 150),   # Bottle medium
    ]

    print("🧪 Distance Estimation Tests:")
    print("─" * 40)
    for label, height in tests:
        distance, danger = estimator.estimate(label, height)
        print(f"  {label:10} | "
              f"bbox_h={height:3} | "
              f"{distance:4}cm | "
              f"{danger}")
    print("─" * 40)

    # Test direction
    print("\n🧪 Direction Tests:")
    print("─" * 40)
    frame_width = 640
    positions = [100, 320, 550]
    for pos in positions:
        direction = estimator.get_direction(frame_width, pos)
        print(f"  Position {pos:3} → {direction}")
    print("─" * 40)
    print("✅ Distance module test done!")