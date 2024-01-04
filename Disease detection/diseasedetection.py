import os
import time
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
from picamera import PiCamera

# Load the model and data
disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')
model = CNN.CNN(39)
model.load_state_dict(torch.load("plant_disease_model_1_latest.pt", map_location=torch.device('cpu')))
model.eval()

def capture_image():
    camera = PiCamera()
    camera.start_preview()
    time.sleep(2)  # Camera warm-up time
    image_path = 'leaf_image.jpg'
    camera.capture(image_path)
    camera.stop_preview()
    camera.close()
    return image_path

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index

def main():
    while True:
        image_path = capture_image()
        pred = prediction(image_path)
        title = disease_info['disease_name'][pred]
        description = disease_info['description'][pred]
        print(f"Disease: {title}\nDescription: {description}")

        time.sleep(86400)  # Wait for 24 hours

if __name__ == '__main__':
    main()
