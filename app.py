from flask import Flask, render_template, request, redirect, url_for
import requests 
from sense_hat import SenseHat
import cv2
import time
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)

# Load the model and data
disease_info = pd.read_csv('data/disease_info.csv', encoding='cp1252')
model = CNN.CNN(39)
model.load_state_dict(torch.load("model/plant_disease_model_1_latest.pt", map_location=torch.device('cpu')))
model.eval()

# Predefine Image path
image_path = 'static/leaf_image.jpg'
sense = SenseHat()

def get_cpu_temp():
    #Extracts the CPU temperature.
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        cpu_temp = float(f.read()) / 1000
    return cpu_temp

def get_calibrated_temp(sense_temp, cpu_temp):
    #Calibrates the temperature from the Sense HAT sensor by subtracting the CPU temperature influence.
    # The factor '0.5' and offset '5' are hypothetical values; you should determine appropriate values through calibration.
    return sense_temp - ((cpu_temp - sense_temp) / 1.5)

@app.route('/')
def index():
    # Load the mock data from the JSON file
    with open('data/test.json', 'r') as file:
        file_content = file.read()
        json_str = "[" + file_content.replace("}\n{", "},\n{") + "]"
        data = json.loads(json_str)
    
    # Extract data for plotting
    time = [datetime.strptime(entry['time'] + ' ' + entry['datetime'], '%H:%M %m/%d/%Y') for entry in data]
    graph_humidity = [entry['humidity'] for entry in data]
    graph_temperature = [entry['temperature'] for entry in data]

    # Create temperature and humidity graphs
    plt.figure(figsize=(10, 5))
    plt.plot(time, graph_temperature, label='Temperature (Â°C)')
    plt.xlabel('Time')
    plt.ylabel('Temperature (Â°C)')
    plt.title('Temperature Over Time')
    plt.grid(True)
    plt.legend()
    plt.savefig('static/temperature_graph.png')
    plt.clf()

    plt.figure(figsize=(10, 5))
    plt.plot(time, graph_humidity, label='Humidity (%)', color='orange')
    plt.xlabel('Time')
    plt.ylabel('Humidity (%)')
    plt.title('Humidity Over Time')
    plt.grid(True)
    plt.legend()  
    plt.savefig('static/humidity_graph.png')

    # Get humidty
    humidity = sense.get_humidity()
    humidity_percentage = "{:.2f}%".format(humidity)
    #humidity_percentage = 20

    # Get temperatures
    temp_from_pressure = sense.get_temperature_from_pressure()
    cpu_temp = get_cpu_temp()
    calibrated_temp_from_pressure = get_calibrated_temp(temp_from_pressure, cpu_temp)
    #calibrated_temp_from_pressure = 18
    return render_template('index.html', humidity=humidity_percentage, temperature=round(calibrated_temp_from_pressure, 1), temperature_graph='temperature_graph.png', humidity_graph='humidity_graph.png')

@app.route('/take-picture', methods=['POST'])
def take_picture():
    capture_image()
    return redirect(url_for('results'))

@app.route('/assess-health', methods=['POST'])
def assess_health():
    # Get humidty
    humidity = sense.get_humidity()
    humidity_percentage = "{:.2f}%".format(humidity)
    #humidity_percentage = 20
 
    # Get temperatures
    temp_from_pressure = sense.get_temperature_from_pressure()
    cpu_temp = get_cpu_temp()
    calibrated_temp_from_pressure = get_calibrated_temp(temp_from_pressure, cpu_temp)
    #calibrated_temp_from_pressure = 18
   
    files = {'file': open(image_path, 'rb')}
    response = requests.post("http://172.20.10.2:5000/predict", files=files)
    prediction_result = response.json()
 
    return render_template('detailedresults.html', humidity=humidity_percentage, temperature=round(calibrated_temp_from_pressure, 1), disease_name=prediction_result['disease_name'])

@app.route('/results')
def results():
    # Get humidty
    humidity = sense.get_humidity()
    humidity_percentage = "{:.2f}%".format(humidity)
    #humidity_percentage = 20

    # Get temperatures
    temp_from_pressure = sense.get_temperature_from_pressure()
    cpu_temp = get_cpu_temp()
    calibrated_temp_from_pressure = get_calibrated_temp(temp_from_pressure, cpu_temp)
    #calibrated_temp_from_pressure = 18

    #prediction(image_path)
    #get_prediction()

    return render_template('results.html', humidity=humidity_percentage, temperature=round(calibrated_temp_from_pressure, 1))

def capture_image():
    camera = cv2.VideoCapture(0)
    time.sleep(2)  # Camera warm-up time
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(image_path, frame)
    camera.release()


def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index

def get_prediction():
    if image_path:
        pred = prediction(image_path)
        title = disease_info['disease_name'][pred]
        description = disease_info['description'][pred]
        return title
    else:
        return "Error", "Unable to capture image."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
