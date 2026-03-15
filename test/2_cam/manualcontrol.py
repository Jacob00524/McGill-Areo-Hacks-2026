import cv2
from drone import *
from led_tracker import LEDTracker
from triangulation import Box3DTracker

# Cameras
front_cam = LEDTracker(camera = 1, threshold = 220)
side_cam = LEDTracker(camera = 2, threshold = 220)

box_tracker = Box3DTracker()

# Drone setup
set_yaw(0)
set_mode(1)

BASE_THRUST = 80

# Control tuning
KP_X = 0.4   # roll
KP_Z = 0.4   # pitch
KP_Y = 0.7   # altitude

TOLERANCE = 1.5  # cm deadzone


# Compute box center
TARGET_X = (box_tracker.x_min_cm + box_tracker.x_max_cm) / 2
TARGET_Y = (box_tracker.y_min_cm + box_tracker.y_max_cm) / 2
TARGET_Z = (box_tracker.z_min_cm + box_tracker.z_max_cm) / 2


def clamp(v, min_val = 0, max_val = 100):
    return max(min_val, min(max_val, v))


def center_drone():

    front_result = front_cam.update()
    side_result = side_cam.update()

    if front_result is None or side_result is None:
        return

    front_frame, _ = front_result
    side_frame, _ = side_result

    front_pos = front_cam.get_position()
    side_pos = side_cam.get_position()

    xyz = box_tracker.compute_xyz(front_pos, side_pos)

    if xyz is None:
        return

    x, y, z = xyz

    # Compute errors relative to center
    error_x = x - TARGET_X
    error_y = y - TARGET_Y
    error_z = z - TARGET_Z

    # Deadzone
    if abs(error_x) < TOLERANCE:
        error_x = 0

    if abs(error_y) < TOLERANCE:
        error_y = 0

    if abs(error_z) < TOLERANCE:
        error_z = 0


    # Convert position error → control adjustments
    roll_adjust = error_x * KP_X
    pitch_adjust = error_z * KP_Z
    thrust_adjust = error_y * KP_Y


    m1 = BASE_THRUST - pitch_adjust - roll_adjust + thrust_adjust # Front left
    m2 = BASE_THRUST - pitch_adjust + roll_adjust + thrust_adjust # Front right
    m3 = BASE_THRUST + pitch_adjust + roll_adjust + thrust_adjust # Back right
    m4 = BASE_THRUST + pitch_adjust - roll_adjust + thrust_adjust # Back left


    # Clamp motor values
    m1 = clamp(m1)
    m2 = clamp(m2)
    m3 = clamp(m3)
    m4 = clamp(m4)

    manual_thrusts(m1, m2, m3, m4)


    # Debug overlay
    cv2.putText(
        front_frame,
        f"X={x:.1f} Y={y:.1f} Z={z:.1f}",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    cv2.imshow("Front Camera", front_frame)
    cv2.imshow("Side Camera", side_frame)

while True:
    center_drone()
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('e'):
        emergency_stop()
        break

