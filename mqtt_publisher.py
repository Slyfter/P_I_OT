import paho.mqtt.publish as publish
from sense_hat import SenseHat
import time
import json
from datetime import datetime

sense = SenseHat()

MQTT_SERVER = "127.0.0.1"
MQTT_TOPIC = "sensor/data"

def get_cpu_temp():
    """Extracts the CPU temperature."""
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        cpu_temp = float(f.read()) / 1000
    return cpu_temp

def get_calibrated_temp(sense_temp, cpu_temp):
    """Calibrates the temperature from the Sense HAT sensor by subtracting the CPU temperature influence."""
    return sense_temp - ((cpu_temp - sense_temp) / 1.5)

def read_temp():
    temp_from_pressure = sense.get_temperature_from_pressure()
    cpu_temp = get_cpu_temp()
    calibrated_temp_from_pressure = get_calibrated_temp(temp_from_pressure, cpu_temp)
    return round(calibrated_temp_from_pressure, 1)

def read_humidity():
    h = sense.get_humidity()
    return round(h, 1)

for i in range(100):
    current_time = datetime.now()
    data = {
        "time": current_time.strftime("%H:%M"),
        "datetime": current_time.strftime("%m/%d/%Y"),
        "humidity": read_humidity(),
        "temperature": read_temp()
    }
    json_data = json.dumps(data)
    publish.single(MQTT_TOPIC, json_data, hostname=MQTT_SERVER)
    time.sleep(600)