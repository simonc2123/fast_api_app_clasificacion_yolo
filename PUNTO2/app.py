from flask import Flask, request, jsonify
from PIL import Image
import io
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import urllib.request

app = Flask(__name__)

# Cargar modelo ResNet18 preentrenado en ImageNet
model = models.resnet18(pretrained=True)
model.eval()

# Transformaciones de imagen requeridas por ResNet18
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Descargar etiquetas de ImageNet
urllib.request.urlretrieve(
    'https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt',
    'imagenet_classes.txt'
)

with open('imagenet_classes.txt') as f:
    classes = [line.strip() for line in f.readlines()]

@app.route('/predict', methods=['POST'])
def predict():
    if 'img' not in request.files:
        return jsonify({'error': 'no image provided'}), 400
    img = Image.open(io.BytesIO(request.files['img'].read())).convert('RGB')
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        outputs = model(tensor)
    _, predicted = torch.max(outputs, 1)
    return jsonify({'prediction': classes[predicted.item()]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
