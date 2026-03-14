import cv2
from led_tracker import LEDTracker

cam = LEDTracker(camera=0, threshold=220)

while True:
    result = cam.update()

    if result is None:
        break

    frame, thresh = result
    pos = cam.get_position()

    if pos is not None:
        x, y = pos
        print(f"X={x}, Y={y}")

        cv2.putText(
            frame,
            f"X={x} Y={y}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    cv2.imshow("Camera 0", frame)
    cv2.imshow("Threshold", thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()