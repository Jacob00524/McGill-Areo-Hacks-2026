import cv2
import numpy as np
import threading

class VisionSystem:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 60) # High FPS is key for stability
        
        self.ret, self.frame = self.cap.read()
        self.stopped = False
        
        # Start a thread to keep reading frames (prevents lag)
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while not self.stopped:
            self.ret, self.frame = self.cap.read()

    def get_drone_position(self, hsv_lower, hsv_upper):
        if not self.ret:
            return None
        
        # 1. Convert to HSV
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        
        # 2. Create a mask (removes everything except the LED color)
        mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
        
        # 3. Clean up noise (Erosion/Dilation)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        # 4. Find the center of the LED "blob"
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Assume the largest blob of that color is our drone
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            if M["m00"] > 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                return (center_x, center_y)
        
        return None

    def stop(self):
        self.stopped = True
        self.cap.release()