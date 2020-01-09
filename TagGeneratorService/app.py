from flask import Flask, jsonify, request
from detector import Detector
from postgres.datalayer.DB_controller import PostgresImageDBController
import json
from torchvision.models.detection import fasterrcnn_resnet50_fpn
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

app = Flask(__name__)
model = fasterrcnn_resnet50_fpn(pretrained=True)
with open('categories.json') as json_file:
    labelMap = json.load(json_file)
detector = Detector(model, labelMap)
postgres = PostgresImageDBController("imagedb","searchservice","admin","localhost")

def send_search_request(tags):
    pass

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
        #TODO: verify url and file he
        img_bytes = file.read()
        class_name = detector.produce_tag(image_bytes=img_bytes)
        postgres.add_image_with_tags(url,class_name)
        return jsonify({'class_name': list(class_name)})

if __name__ == '__main__':
    app.run(port="8888")