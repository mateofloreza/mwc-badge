import cv2

camera = cv2.VideoCapture(0)  # Try 1, 2, or 3 if 0 fails
if not camera.isOpened():
    print("Error: Cannot access the camera")
else:
    print("Camera accessed successfully")

