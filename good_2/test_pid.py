from controller import controller

def main():
    # Example current drone state
    state = {
        "x": 64,          # meters
        "y": 3,
        "z": 34,

        "vx": 0.00,         # m/s
        "vy": 0.00,
        "vz": -0.02,

        "roll": 0.05,       # radians
        "pitch": -0.03,

        "roll_rate": 0.00,  # rad/s
        "pitch_rate": 0.00,
    }

    # Desired hover point
    ref = {
        "x": 0.00,
        "y": 10.0,
        "z": 0.00,
    }

    motors = controller(state, ref)

    print("Current state:")
    for k, v in state.items():
        print(f"  {k}: {v}")

    print("\nReference:")
    for k, v in ref.items():
        print(f"  {k}: {v}")

    print("\nMotor commands:")
    for i, m in enumerate(motors, start=1):
        print(f"  m{i}: {m:.4f}")


if __name__ == "__main__":
    main()