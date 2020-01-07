from flask import Flask, jsonify, request
from detector import Detector
import json
from torchvision.models.detection import fasterrcnn_resnet50_fpn
app = Flask(__name__)

model = fasterrcnn_resnet50_fpn(pretrained=True)
with open('categories.json') as json_file:
    labelMap = json.load(json_file)
detector = Detector(model, labelMap)

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        class_name = detector.produce_tag(image_bytes=img_bytes)
        return jsonify({'class_name': list(class_name)})
@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        file = request.files['file']
        url = request.form['url']
        img_bytes = file.read()
        class_name = detector.produce_tag(image_bytes=img_bytes)
        return jsonify({'class_name': list(class_name)})
if __name__ == '__main__':
    app.run(port="8888")