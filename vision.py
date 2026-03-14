import cv2
import numpy as np

class LEDTracker:
    def __init__(self):
        # Index 0 is usually your primary camera
        self.cap = cv2.VideoCapture(0)
        
        # Tuning the Green LED range:
        # Hue: 40-80 (Green) | Saturation: 100-255 | Value: 100-255
        self.lower_green = np.array([40, 100, 100])
        self.upper_green = np.array([80, 255, 255])
        
        self.current_x = None
        self.current_y = None

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        # 1. BGR to HSV conversion
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 2. Thresholding (The Mask)
        mask = cv2.inRange(hsv, self.lower_green, self.upper_green)
        
        # 3. Noise reduction (Removes tiny random bright spots)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # 4. Find the LED position
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Assume the largest green blob is our drone
            best_cnt = max(contours, key=cv2.contourArea)
            M = cv2.moments(best_cnt)
            if M["m00"] > 0:
                self.current_x = int(M["m10"] / M["m00"])
                self.current_y = int(M["m01"] / M["m00"])
                
                # Draw a circle on the frame so we can see it working
                cv2.circle(frame, (self.current_x, self.current_y), 10, (0, 255, 0), 2)
        else:
            self.current_x, self.current_y = None, None

        return frame, mask

    def get_position(self):
        return self.current_x, self.current_y

    def release(self):
        self.cap.release()