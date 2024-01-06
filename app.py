from flask import Flask, render_template, request, redirect, url_for
import cv2
import time

app = Flask(__name__)

# Dummy data for environmental info
environmental_info = {
    'temperature': '25 °C',
    'humidity': '40%'
}

@app.route('/')
def index():
    return render_template('index.html', info=environmental_info)

@app.route('/take-picture', methods=['POST'])
def take_picture():
    capture_image()
    return redirect(url_for('results'))

@app.route('/results')
def results():
    return render_template('results.html', info=environmental_info)

def capture_image():
    camera = cv2.VideoCapture(0)
    time.sleep(2)  # Camera warm-up time
    ret, frame = camera.read()
    if ret:
        cv2.imwrite('static/leaf_image.jpg', frame)
    camera.release()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
