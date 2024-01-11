from flask import Flask, request, jsonify
import CNN
import torch
import torchvision.transforms.functional as TF
from PIL import Image
import numpy as np
import pandas as pd
 
app = Flask(__name__)
 
# Load model and data (similar to Raspberry Pi's app)
disease_info = pd.read_csv('data/disease_info.csv', encoding='cp1252')
model = CNN.CNN(39)
model.load_state_dict(torch.load("model/plant_disease_model_1_latest.pt", map_location=torch.device('cpu')))
model.eval()
 
@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    image = Image.open(file.stream)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    title = disease_info['disease_name'][index]
    return jsonify({'disease_name': title})
 
if __name__ == '__main__':
    app.run(debug=True, host='192.168.8.111', port=5000)