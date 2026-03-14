from drone import *
import triangulation


x, y, z = triangulation.compute_xyz(self, front_pos, side_pos)
def center_drone():
    manual_thrusts(60, 60, 60, 60)
    while True:
    # Slowly increase thrust to lift off
        if y < 240:
            increment_thrusts(10,10,10,10)
        if y > 240:
           increment_thrusts(-10,-10,-10,-10) 
        if y = 240:
            return None




