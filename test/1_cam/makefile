# --- Variables ---
PYTHON = python3
MAIN = main.py
CONFIG = config.py

# --- Default Goal ---
.DEFAULT_GOAL := help

# --- Targets ---

## 1. Connection Check
# Checks if the ESP32-S2 is actually reachable over the network
check-connection:
       @echo "Checking link to ESP32-S2 (192.168.4.1)..."
       @ping -c 2 192.168.4.1 > /dev/null || (echo "ERROR: Drone not found. Connect to Drone Wi-Fi!" && exit 1)
       @echo "Connection [OK]"

## 2. Setup (Install dependencies if needed)
setup:
       @echo "Installing OpenCV and NumPy..."
       $(PYTHON) -m pip install opencv-python numpy

## 3. THE RUN COMMAND
# This is what you use for the official judged attempt.
# It checks the connection first, then launches the flight loop.
run: check-connection
       @echo "------------------------------------------------"
       @echo "LAUNCHING VISION-BASED AUTONOMOUS HOVER"
       @echo "Press 'Q' in the window to Emergency Stop."
       @echo "------------------------------------------------"
      $(PYTHON) $(MAIN)

## 4. Calibration Mode
# Useful for finding the Green LED HSV values right before the run
calibrate:
       @echo "Launching HSV Calibration Tool..."
       $(PYTHON) led_tracker.py --calibrate

## 5. Emergency Stop (Software Level)
# Forces all python processes to stop if the terminal hangs
kill:
       @pkill -f $(PYTHON) || echo "No processes to kill."

## 6. Help
help:
       @echo "Available commands:"
       @echo "  make run              - Run the full autonomous flight"
       @echo "  make check-connection - Verify Wi-Fi link to drone"
       @echo "  make calibrate        - Test LED tracking without flying"
       @echo "  make setup            - Install required libraries"