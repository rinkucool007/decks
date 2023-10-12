pip install picamera flask

import io
import picamera
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the Raspberry Pi Camera Stream!'

def generate():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24

        # Wait for the camera to warm up
        time.sleep(2)

        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')
            stream.seek(0)
            stream.truncate()

@app.route('/video')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)



python streaming.py


http://<your_pi_ip>:8080/video
