import cv2

# Replace 'localhost' with the appropriate server IP if needed.
stream_url = 'http://localhost:5000/video_feed'

# Open the video stream from the Flask server
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Display the frame in a window named 'Video Stream'
    cv2.imshow('Video Stream', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
