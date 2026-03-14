import drone 
import time

print(drone.get_firmware_version())

drone.green_LED(0)

time.sleep(1)

drone.green_LED(1)

time.sleep(2)

drone.green_LED(0)

time.sleep(1)

drone.green_LED(1)