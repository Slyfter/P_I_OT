import cv2
import time
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd

# Load the model and data
disease_info = pd.read_csv('Disease detection/data/disease_info.csv', encoding='cp1252')
model = CNN.CNN(39)
model.load_state_dict(torch.load("Disease detection/model/plant_disease_model_1_latest.pt", map_location=torch.device('cpu')))
model.eval()

def capture_image():
    camera = cv2.VideoCapture(0)  # Assuming the USB camera is the first camera
    ret, frame = camera.read()
    if ret:
        image_path = 'Disease detection/leaf_image.jpg'
        cv2.imwrite(image_path, frame)
    camera.release()
    return image_path if ret else None

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
    image_path = capture_image()
    if image_path:
        pred = prediction(image_path)
        title = disease_info['disease_name'][pred]
        description = disease_info['description'][pred]
        return title, description
    else:
        return "Error", "Unable to capture image."

if __name__ == '__main__':
    title, description = get_prediction()
    print(f"Disease: {title}\nDescription: {description}")
