from vision import LEDTracker

tracker = LEDTracker()

while True:
    frame = tracker.update()

    x, y = tracker.get_position()

    if x is not None:
        print("LED:", x, y)