import cv2
import numpy as np

class LEDTracker:
    def __init__(self, camera=0, threshold=220):
        self.cap = cv2.VideoCapture(camera)
        self.threshold = threshold
        self.x = None
        self.y = None

    def update(self):
        """Process one frame and update LED position."""
        ret, frame = self.cap.read()
        if not ret:
            return None

        blurred = cv2.GaussianBlur(frame, (9, 9), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY)

        kernel = np.ones((3,3), np.uint8)
        thresh = cv2.erode(thresh, kernel, iterations=1)
        thresh = cv2.dilate(thresh, kernel, iterations=2)

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:
            largest = max(contours, key=cv2.contourArea)

            if cv2.contourArea(largest) > 5:
                M = cv2.moments(largest)

                if M["m00"] != 0:
                    self.x = int(M["m10"] / M["m00"])
                    self.y = int(M["m01"] / M["m00"])

        return frame

    def get_position(self):
        """Poll the latest LED position."""
        return self.x, self.y

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
