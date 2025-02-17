from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

def generate_frames():
    RTSP_URL = "rtsp://192.168.0.14:8554/live"
    camera = cv2.VideoCapture(RTSP_URL)  # Ensure camera is opened correctly
    while True:
        success, frame = camera.read()  # Read a frame from the camera
        if not success:
            continue  # Skip this frame if read fails
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

