import cv2
import time

from led_tracker import LEDTracker
from triangulation import Box3DTracker
from drone import *
from controller import controller


front_cam = LEDTracker(camera=0, threshold=220)
side_cam = LEDTracker(camera=1, threshold=220)

box_tracker = Box3DTracker()

set_mode(1)  # manual motor control


x_prev = y_prev = z_prev = None
t_prev = time.time()


ref = {
    "x": 0.0,
    "y": 30.0,
    "z": 0.0,   # example hover height (cm)
}

green_LED(255)

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
        print(f"X={x:.2f} Y={y:.2f} Z={z:.2f}")

        # time step
        t = time.time()
        dt = t - t_prev
        t_prev = t

        # velocity estimate
        if x_prev is None:
            vx = vy = vz = 0
        else:
            vx = (x - x_prev) / dt
            vy = (y - y_prev) / dt
            vz = (z - z_prev) / dt

        x_prev, y_prev, z_prev = x, y, z

        # drone attitude
        roll = get_roll()
        pitch = get_pitch()

        roll_rate = get_gyro_roll()
        pitch_rate = get_gyro_pitch()

        state = {
            "x": x,
            "y": y,
            "z": z,

            "vx": vx,
            "vy": vy,
            "vz": vz,

            "roll": roll,
            "pitch": pitch,

            "roll_rate": roll_rate,
            "pitch_rate": pitch_rate
        }

        motors = controller(state, ref)

        # clamp motor values
        motors = [max(0, min(250, int(m))) for m in motors]

        # send to drone
        manual_thrusts(motors[0], motors[1], motors[2], motors[3])

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

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('e'):
        emergency_stop()
        break


front_cam.release()
side_cam.release()
cv2.destroyAllWindows()