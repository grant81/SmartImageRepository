from flask import Flask, jsonify, request
from detector import Detector
from DB_controller import PostgresImageDBController
import json
from torchvision.models.detection import fasterrcnn_resnet50_fpn
import logging
import requests
import torch
import os
import redis

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

SEARCH_SERVICE_HOST = os.environ['SEARCH_SERVICE_HOST']
STATE_DICT_PATH = 'model/fasterrcnn_resnet50_fpn_coco-258fb6c6.pth'

# this is here for easier unit testing
detector = None
postgres = None
redis_client = None


def send_search_request(tags):
    url = "http://%s:8889/search" % SEARCH_SERVICE_HOST
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


def initialize():
    global detector, postgres, redis_client
    model = fasterrcnn_resnet50_fpn(pretrained=False)
    model.load_state_dict(torch.load(STATE_DICT_PATH))
    with open('categories.json') as json_file:
        labelMap = json.load(json_file)
    detector = Detector(model, labelMap)
    postgres = PostgresImageDBController(os.environ['POSTGRES_DB'], os.environ['POSTGRES_USER'],
                                         os.environ['POSTGRES_PASSWORD'], os.environ['POSTGRES_HOST'])
    redis_client = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'],
                                     password=os.environ['REDIS_PASSWORD'], decode_responses=True)


def create_app():
    app = Flask(__name__)

    @app.route('/search', methods=['POST'])
    def search():
        if request.method == 'POST':
            file = request.files['file']
            img_bytes = file.read()
            tags = detector.produce_tag(image_bytes=img_bytes)
            tags.sort()
            # check tags in cache, if it is there, no need to talk to searcher
            redis_key = str(tags)
            result = redis_client.lrange(redis_key, 0, -1)
            if result:
                return jsonify({'urls': result})
            return send_search_request(tags)

    @app.route('/save', methods=['POST'])
    def save():
        if request.method == 'POST':
            file = request.files['file']
            img_bytes = file.read()
            url = request.form['url']
            class_name = detector.produce_tag(image_bytes=img_bytes)
            postgres.add_image_with_tags(url, class_name)
            return jsonify({'tags': list(class_name)})

    return app


if __name__ == '__main__':
    initialize()
    app = create_app()
    app.run(host='0.0.0.0', port="8888")
