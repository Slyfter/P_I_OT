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

1. Clone this repository to your Raspberry Pi:

```bash
git clone https://github.com/your-username/plant-iot-dashboard.git
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Connect your Raspberry Pi to the Sense HAT and the camera.

4. Run the Flask application:

```bash
flask run
```

5. Access the dashboard by opening a web browser and navigating to `http://your-pi-ip-address:5000`.

## Usage

- The dashboard displays real-time temperature and humidity data.
- Click the "Assess Health" button to capture an image of your plant to detect any leaf diseases of your plant. 







