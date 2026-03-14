import cv2
from vision import LEDTracker

tracker = LEDTracker()

while True:
    result = tracker.update()
    if result is None:
        break

    frame, thresh = result
    x, y = tracker.get_position()

    if x is not None:
        print(f"LED position: ({x}, {y})")

    cv2.imshow("Drone LED Tracking", frame)
    cv2.imshow("Threshold", thresh)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

tracker.release()