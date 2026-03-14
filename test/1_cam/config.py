t   # --- Camera & Vision ---
CAM_FRONT_ID = 0
CAM_SIDE_ID = 1
# Green LED HSV values (Adjust during on-site calibration)
GREEN_LOWER = [40, 100, 100]
GREEN_UPPER = [80, 255, 255]

# --- Physical Space (1m x 1m x 1m cage) ---
# Conversion: Meters / Pixel (Example: 1m / 640px)
M_PER_PX = 0.00156 
HOVER_HEIGHT_M = 0.5
TARGET_X_PX = 320  # Center of 640px width
TARGET_Y_PX = 320  # Center of 640px width (Side cam)

# --- PID Gains ---
# Start low (0.1) and increase slowly
KP_X, KI_X, KD_X = 0.5, 0.01, 0.1
KP_Y, KI_Y, KD_Y = 0.5, 0.01, 0.1
KP_Z, KI_Z, KD_Z = 0.8, 0.05, 0.2