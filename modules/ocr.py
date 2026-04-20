import cv2
import pytesseract
import numpy as np
import os
import re

# Windows Tesseract path
pytesseract.pytesseract.tesseract_cmd = \
    r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set tessdata prefix
os.environ['TESSDATA_PREFIX'] = \
    r'C:\Program Files\Tesseract-OCR\tessdata'

class TextReader:
    def __init__(self):
        self.last_text     = ""
        self.min_length    = 8     # Ignore short text
        self.min_words     = 2     # Need at least 2 words
        self.min_conf      = 60    # Confidence threshold
        print("✅ Text Reader ready!")

    def preprocess(self, frame):
        """
        Clean image for better OCR accuracy
        """
        # Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Resize for better OCR
        gray = cv2.resize(
            gray, None,
            fx=2, fy=2,
            interpolation=cv2.INTER_CUBIC
        )

        # Remove noise
        blur = cv2.GaussianBlur(gray, (3, 3), 0)

        # Binarize
        thresh = cv2.threshold(
            blur, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        return thresh

    def is_valid_text(self, text):
        """
        Filter out random/meaningless text
        """
        if not text:
            return False

        # Must be long enough
        if len(text) < self.min_length:
            return False

        # Must have at least 2 words
        words = text.split()
        if len(words) < self.min_words:
            return False

        # Must have enough real letters
        letters = sum(c.isalpha() for c in text)
        total   = len(text.replace(' ', ''))
        if total == 0:
            return False

        # At least 60% must be letters
        letter_ratio = letters / total
        if letter_ratio < 0.6:
            return False

        # No random symbol strings
        if re.search(r'[^a-zA-Z0-9\s.,!?-]', text):
            # Too many special chars
            special = sum(
                not c.isalnum() and c != ' '
                for c in text
            )
            if special > len(text) * 0.2:
                return False

        return True

    def read_text(self, frame):
        """
        Extract meaningful text from frame
        Returns cleaned text or None
        """
        # Preprocess
        clean = self.preprocess(frame)

        # OCR with confidence data
        data = pytesseract.image_to_data(
            clean,
            config='--oem 3 --psm 6',
            lang='eng',
            output_type=pytesseract.Output.DICT
        )

        # Collect high confidence words only
        good_words = []
        for i, word in enumerate(data['text']):
            conf = int(data['conf'][i])
            word = word.strip()

            # Only keep high confidence words
            if conf >= self.min_conf and len(word) > 1:
                good_words.append(word)

        # Join words
        text = ' '.join(good_words)
        text = text.strip()

        # Validate text
        if self.is_valid_text(text):
            if text != self.last_text:
                self.last_text = text
                return text

        return None

    def draw_text_box(self, frame, text):
        """
        Draw found text on frame
        """
        if not text:
            # Show waiting message
            cv2.rectangle(
                frame,
                (0, frame.shape[0] - 60),
                (frame.shape[1], frame.shape[0]),
                (0, 0, 0), -1
            )
            cv2.putText(
                frame,
                "Point camera at text...",
                (10, frame.shape[0] - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (128, 128, 128), 2
            )
            return frame

        # Background box
        cv2.rectangle(
            frame,
            (0, frame.shape[0] - 80),
            (frame.shape[1], frame.shape[0]),
            (0, 0, 0), -1
        )

        # Show text
        cv2.putText(
            frame,
            f"Text: {text[:50]}",
            (10, frame.shape[0] - 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 255, 0), 2
        )

        return frame


# ── Test ─────────────────────────────────────────────────
if __name__ == "__main__":

    # Verify Tesseract
    print("🔄 Checking Tesseract...")
    try:
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract version: {version}")
    except Exception as e:
        print(f"❌ Tesseract error: {e}")
        exit()

    reader = TextReader()
    cap    = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not found!")
        exit()

    print("\n📷 Camera started!")
    print("─" * 40)
    print("  Point camera at clear text")
    print("  Best results:")
    print("  → Book cover")
    print("  → Product label")
    print("  → Printed paper")
    print("  Q → Quit")
    print("─" * 40)

    current_text = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Read text
        text = reader.read_text(frame)

        if text:
            current_text = text
            print(f"\n📖 Found: {text}")

        # Draw on frame
        frame = reader.draw_text_box(frame, current_text)

        # Show instructions
        cv2.putText(
            frame,
            "OCR MODE - Point at text",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (0, 255, 0), 2
        )

        cv2.imshow("Text Reader Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ OCR test done!")