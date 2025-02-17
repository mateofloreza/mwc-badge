from flask import Flask, Response
import cv2
import subprocess

app = Flask(__name__)

# Update the camera index
camera_index = 0
video_capture = cv2.VideoCapture(camera_index)

if not video_capture.isOpened():
    raise RuntimeError(f"Failed to open camera {camera_index}. Please check the camera connection.")

# Route to stream video
@app.route('/video_feed')
def video_feed():
    def generate_frames():
        # Use ffmpeg for real-time H.264 encoding
        ffmpeg_command = [
            'ffmpeg',
            '-y',                     # Overwrite output files
            '-f', 'rawvideo',         # Input format
            '-vcodec', 'rawvideo',    # Codec for raw video input
            '-pix_fmt', 'bgr24',      # Pixel format
            '-s', f"{int(video_capture.get(3))}x{int(video_capture.get(4))}",  # Frame size
            '-r', '30',               # Frame rate
            '-i', '-',                # Input from stdin
            '-an',                    # No audio
            '-vcodec', 'libx264',     # Output codec
            '-preset', 'ultrafast',   # Low-latency preset
            '-tune', 'zerolatency',   # Optimize for low latency
            '-f', 'mp4',              # Output format
            'pipe:1'                  # Output to stdout
        ]

        process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while True:
            success, frame = video_capture.read()
            if not success:
                break
            process.stdin.write(frame.tobytes())
            yield process.stdout.read(1024)  # Stream data in chunks

    return Response(generate_frames(), mimetype='video/mp4')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)
