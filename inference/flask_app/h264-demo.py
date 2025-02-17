from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

def generate_frames():
    #RTSP_URL = "http://192.168.0.14:6000/video_feed"  # Your server URL
    RTSP_URL = "rtsp://192.168.178.25:8554/video_feed"
    # Open the video feed (this should work if your Flask server is streaming the video properly)
    camera = cv2.VideoCapture(RTSP_URL)
    
    if not camera.isOpened():
        raise RuntimeError(f"Failed to open video stream from {RTSP_URL}")
    
    while True:
        success, frame = camera.read()  # Read a frame from the stream
        if not success:
            continue  # Skip if frame read fails
        
        # Encode the frame as JPEG for efficient transmission
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue  # Skip if encoding fails

        frame = buffer.tobytes()

        # Yield the frame in the multipart format expected by browsers
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')  # Your HTML template

@app.route('/video_feed')
def video_feed():
    # This route will stream the frames to the browser in MJPEG format
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

