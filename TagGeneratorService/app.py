from flask import Flask, jsonify, request
from detector import Detector
from DB_controller import PostgresImageDBController
import json
from torchvision.models.detection import fasterrcnn_resnet50_fpn
import logging
import requests

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

app = Flask(__name__)
model = fasterrcnn_resnet50_fpn(pretrained=True)
with open('categories.json') as json_file:
    labelMap = json.load(json_file)
detector = Detector(model, labelMap)
postgres = PostgresImageDBController("imagedb", "searchservice", "admin", "localhost")


def send_search_request(tags):
    url = "http://localhost:8889/search"
    headers = {
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "localhost:8889",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    data = {'tags': tags}
    response = requests.request("GET", url, json=data, headers=headers)
    if response.status_code > 300:
        logging.error("failed to get a response from search engine")
        return []
    return response.json()


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        tags = detector.produce_tag(image_bytes=img_bytes)
        return send_search_request(tags)

@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        file = request.files['file']
        url = request.form['url']
        img_bytes = file.read()
        class_name = detector.produce_tag(image_bytes=img_bytes)
        postgres.add_image_with_tags(url, class_name)
        return jsonify({'class_name': list(class_name)})


if __name__ == '__main__':
    app.run(port="8888")
