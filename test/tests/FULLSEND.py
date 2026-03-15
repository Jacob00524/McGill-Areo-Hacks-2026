import drone
import time
import cv2

drone.green_LED(0)
drone.recalibrate()
time.sleep(1) # 15

drone.set_mode(1)
drone.green_LED(1)

drone.set_yaw(0)

drone.manual_thrusts(50, 50, 50, 50)
time.sleep(1)
drone.manual_thrusts(100, 100, 100, 100)
time.sleep(1)

m1 = 150
m2 = 150
m3 = 150
m4 = 150

while True:
    drone.manual_thrusts(m1, m2, m3, m4)


    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('e'):
        drone.emergency_stop()
        break
    elif key == ord('f'):
        if m1 < 250:
            m1 += 50
            m2 += 50
            m3 += 50
            m4 += 50
