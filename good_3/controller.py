hover_thrust = 0.5


class PD:
    def __init__(self, kp, kd):
        self.kp = kp
        self.kd = kd

    def update(self, error, rate):
        return self.kp * error - self.kd * rate


# Position controllers
pos_x = PD(0.8, 0.3)
pos_y = PD(0.8, 0.3)
pos_z = PD(1.2, 0.4)

# Attitude controllers
att_roll = PD(4.0, 0.15)
att_pitch = PD(4.0, 0.15)


def controller(state, ref):

    x, y, z = state["x"], state["y"], state["z"]
    vx, vy, vz = state["vx"], state["vy"], state["vz"]

    roll, pitch = state["roll"], state["pitch"]
    roll_rate = state["roll_rate"]
    pitch_rate = state["pitch_rate"]

    x_ref, y_ref, z_ref = ref["x"], ref["y"], ref["z"]

    # position errors
    ex = x_ref - x
    ey = y_ref - y
    ez = z_ref - z

    # outer loop: position -> desired tilt
    pitch_ref = pos_x.update(ex, vx)
    roll_ref = pos_y.update(ey, vy)

    thrust = hover_thrust + pos_z.update(ez, vz)

    # inner loop: attitude stabilization
    e_roll = roll_ref - roll
    e_pitch = pitch_ref - pitch

    u_roll = att_roll.update(e_roll, roll_rate)
    u_pitch = att_pitch.update(e_pitch, pitch_rate)

    # motor mix (no yaw term)
    m1 = thrust + u_roll + u_pitch
    m2 = thrust - u_roll + u_pitch
    m3 = thrust - u_roll - u_pitch
    m4 = thrust + u_roll - u_pitch

    return [m1, m2, m3, m4]