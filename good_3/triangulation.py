def map_range(value, in_min, in_max, out_min, out_max):
    return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)


class Box3DTracker:
    def __init__(self):
        # Example calibration values — replace with your real ones

        # Front camera: pixel -> x,y
        self.front_x_min_px = 0
        self.front_x_max_px = 1920
        self.front_y_min_px = 0
        self.front_y_max_px = 1080

        self.x_min_cm = 0.0
        self.x_max_cm = 100.0
        self.y_min_cm = 0.0
        self.y_max_cm = 100.0

        # Side camera: pixel -> z,y
        self.side_z_min_px = 0.0
        self.side_z_max_px = 100.0
        self.side_y_min_px = 0.0
        self.side_y_max_px = 100.0

        self.z_min_cm = 0.0
        self.z_max_cm = 100.0

    def compute_xyz(self, front_pos, side_pos):
        fx, fy = front_pos
        sx, sy = side_pos

        if fx is None or fy is None or sx is None or sy is None:
            return None

        x = map_range(
            fx,
            self.front_x_min_px, self.front_x_max_px,
            self.x_min_cm, self.x_max_cm
        )

        y_front = map_range(
            fy,
            self.front_y_min_px, self.front_y_max_px,
            self.y_min_cm, self.y_max_cm
        )

        y_side = map_range(
            sy,
            self.side_y_min_px, self.side_y_max_px,
            self.y_min_cm, self.y_max_cm
        )

        z = map_range(
            sx,
            self.side_z_min_px, self.side_z_max_px,
            self.z_min_cm, self.z_max_cm
        )

        # Average y from both cameras
        y = (y_front + y_side) / 2.0

        return x, y, z