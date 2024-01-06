from flask import Flask, render_template, request, redirect, url_for
from sense_hat import SenseHat
import cv2
import time

app = Flask(__name__)
sense = SenseHat()

def get_cpu_temp():
    """Extracts the CPU temperature."""
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        cpu_temp = float(f.read()) / 1000
    return cpu_temp

def get_calibrated_temp(sense_temp, cpu_temp):
    """Calibrates the temperature from the Sense HAT sensor by subtracting the CPU temperature influence."""
    # The factor '0.5' and offset '5' are hypothetical values; you should determine appropriate values through calibration.
    return sense_temp - ((cpu_temp - sense_temp) / 1.5)

@app.route('/')
def index():
    # Get humidty
    humidity = sense.get_humidity()
    humidity_percentage = "{:.2f}%".format(humidity)

    # Get temperatures
    temp_from_pressure = sense.get_temperature_from_pressure()
    cpu_temp = get_cpu_temp()
    calibrated_temp_from_pressure = get_calibrated_temp(temp_from_pressure, cpu_temp)
    return render_template('index.html', humidity=humidity_percentage, temperature=round(calibrated_temp_from_pressure, 1))

@app.route('/take-picture', methods=['POST'])
def take_picture():
    capture_image()
    return redirect(url_for('results'))

@app.route('/results')
def results():
    # Get humidty
    humidity = sense.get_humidity()
    humidity_percentage = "{:.2f}%".format(humidity)

    # Get temperatures
    temp_from_pressure = sense.get_temperature_from_pressure()
    cpu_temp = get_cpu_temp()
    calibrated_temp_from_pressure = get_calibrated_temp(temp_from_pressure, cpu_temp)
    return render_template('results.html', humidity=humidity_percentage, temperature=round(calibrated_temp_from_pressure, 1))

def capture_image():
    camera = cv2.VideoCapture(0)
    time.sleep(2)  # Camera warm-up time
    ret, frame = camera.read()
    if ret:
        cv2.imwrite('static/leaf_image.jpg', frame)
    camera.release()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
