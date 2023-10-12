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

--------------------------------------

pip install flask


from flask import Flask, render_template, Response
import picamera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)  # Adjust the resolution as needed
        camera.framerate = 30  # Adjust the framerate as needed

        while True:
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                stream.seek(0)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')
                stream.seek(0)
                stream.truncate()

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)



index.html

<!DOCTYPE html>
<html>
  <head>
    <title>Raspberry Pi Video Streaming</title>
  </head>
  <body>
    <img src="{{ url_for('video_feed') }}" width="640" height="480">
  </body>
</html>


python stream_video.py
.
