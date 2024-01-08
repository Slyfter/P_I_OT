# P(I)oT Dashboard

## Introduction

This repository contains the code and resources for a Plant IoT Dashboard for monitoring the health and environmental conditions of your plants in real-time. The dashboard provides information about temperature, humidity, and allows you to capture images of your plants in order to assess it's health with a pre-trained machine learning model for image classification.

## Features

- Real-time temperature monitoring
- Real-time humidity monitoring
- Capture images of your plants
- Health assessment of your plants

## Getting Started

Follow these steps to set up the Plant IoT Dashboard on your Raspberry Pi:

1. Install git lfs and clone this repository to your Raspberry Pi:
```bash
sudo apt-get install git-lfs
```

```bash
git lfs clone https://github.com/Slyfter/P_I_OT.git
```

2. Create virtual env and install the required packages:
```bash
sudo apt-get update
sudo apt-get install python3-venv python3-pip
python3 -m venv myenv
source myenv/bin/activate
```

```bash
pip install -r requirements.txt
```

3. Connect your Raspberry Pi to the Sense HAT and the camera.

4. Run the MQTT publisher:<br />
Open the terminal on your raspberry pi and change the directory to the directory where your mqtt_publisher.py is located and run the following command
```bash
python mqtt_publisher.py
```

5. Run the Flask application:<br />
Open the terminal on your raspberry pi and change the directory to the directory where your app.py is located and run the following command
```bash
FLASK_APP=app.py flask run
```

6. Access the dashboard by opening a web browser and navigating to `http://your-pi-ip-address:5000`.

## Usage

- The dashboard displays real-time temperature and humidity data.
- Click the "Assess Health" button to capture an image of your plant to detect any leaf diseases of your plant. 







