import cv2
from flask import Flask, Response, render_template

app = Flask(__name__, template_folder='template')

# URL of the raw video stream server
RAW_STREAM_URL = 'http://localhost:5000/video_feed'

def generate_processed_frames():
    # Connect to the raw video stream
    cap = cv2.VideoCapture(RAW_STREAM_URL)
    if not cap.isOpened():
        print("Error: Could not open the raw video stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # --- Post-processing: simulate YOLO bounding box ---
        height, width, _ = frame.shape
        cv2.rectangle(frame, (50, 50), (width - 50, height - 50), (0, 255, 0), 2)
        # -----------------------------------------------------

        # Encode the processed frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/')
def index():
    # Serve the HTML page that shows the processed video stream.
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Serve the processed frames as an MJPEG stream.
    return Response(generate_processed_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
