import os
import pandas as pd
from PIL import Image
import torchvision.transforms.functional as TF
import numpy as np
import torch
# Assuming CNN.py is in the same directory as this script
import CNN

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Paths to the data and model directories
csv_path = os.path.join(script_dir, 'data', 'disease_info.csv')
model_path = os.path.join(script_dir, 'model', 'plant_disease_model_1_latest.pt')

# Load the model and data
disease_info = pd.read_csv(csv_path, encoding='cp1252')
model = CNN.CNN(39)  # Make sure this matches the CNN definition in CNN.py
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index

def test_model(image_folder, image_name):
    image_path = os.path.join(script_dir, image_folder, image_name)
    pred = prediction(image_path)
    title = disease_info['disease_name'][pred]
    description = disease_info['description'][pred]
    print(f"Disease: {title}\nDescription: {description}")

if __name__ == '__main__':
    # Test with a specific image from the 'images' folder
    test_model('images', 'basil_unhealthy_1.jpg')  # Ensure 'basil_healthy.jpg' is the correct image file name
