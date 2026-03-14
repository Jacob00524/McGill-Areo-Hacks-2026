import cv2
from led_tracker import LEDTracker
from triangulation import Box3DTracker
import drone
from controller import controller
import time

ref = {
    "x": 0.0,
    "y": 50.0, # hover height (cm)
    "z": 0.0,
}

front_cam = LEDTracker(camera=1, threshold=220)
side_cam = LEDTracker(camera=2, threshold=220)

box_tracker = Box3DTracker()

drone.green_LED(0)
#recalibrate()
#time.sleep(15)

time.sleep(2)

drone.set_mode(1)
drone.green_LED(1)

t_prev = time.time()
x_prev = -1
y_prev = -1
z_prev = -1

while True:
    front_result = front_cam.update()
    side_result = side_cam.update()

    if front_result is None or side_result is None:
        print("Error fetching view from camera")
        break

    front_frame = front_result
    side_frame = side_result

    front_pos = front_cam.get_position()
    side_pos = side_cam.get_position()

    xyz = box_tracker.compute_xyz(front_pos, side_pos)

    if xyz is None:
        print("None.")
        continue
    x, y, z = xyz
    print(f"X={x:.2f} Y={y:.2f} Z={z:.2f}")

    # Approx. velocity
    t = time.time()
    if (x_prev == -1 and y_prev == -1 and z_prev == -1):
        t_prev = t
        continue
    x_prev = x
    y_prev = y
    z_prev = z
    dt = t - t_prev
    vx = (x - x_prev) / dt
    vy = (y - y_prev) / dt
    vz = (z - z_prev) / dt

    roll = drone.get_roll()
    pitch = drone.get_pitch()

    roll_rate = drone.get_gyro_roll()
    pitch_rate = drone.get_gyro_pitch()

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
    motors = [max(0, min(250, int(m))) for m in motors]
    # manual_thrusts(motors[0], motors[1], motors[2], motors[3])
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
        drone.emergency_stop()
        break

front_cam.release()
side_cam.release()
cv2.destroyAllWindows()