import cv2
from led_tracker import LEDTracker
from triangulation import Box3DTracker

front_cam = LEDTracker(camera=0, threshold=220)
side_cam = LEDTracker(camera=1, threshold=220)

box_tracker = Box3DTracker()

while True:
    front_result = front_cam.update()
    side_result = side_cam.update()

    if front_result is None or side_result is None:
        break

    front_frame, front_thresh = front_result
    side_frame, side_thresh = side_result

    front_pos = front_cam.get_position()
    side_pos = side_cam.get_position()

    xyz = box_tracker.compute_xyz(front_pos, side_pos)

    if xyz is not None:
        x, y, z = xyz
        print(f"X={x:.2f} cm, Y={y:.2f} cm, Z={z:.2f} cm")

        cv2.putText(
            front_frame,
            f"X={x:.1f} Y={y:.1f} Z={z:.1f}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    cv2.imshow("Front Camera", front_frame)
    cv2.imshow("Side Camera", side_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

front_cam.release()
side_cam.release()
cv2.destroyAllWindows()
