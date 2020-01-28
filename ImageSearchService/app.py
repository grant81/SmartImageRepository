from flask import Flask, jsonify, request
import logging
from searcher import Searcher
import os
from DB_controller import PostgresImageDBController
import redis

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
app = Flask(__name__)


@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        content = request.get_json()
        out = searchEngine.search_keywords(content['tags'])
        return jsonify({'urls': out})


if __name__ == '__main__':
    dbConnection = PostgresImageDBController(os.environ['POSTGRES_DB'], os.environ['POSTGRES_USER'],
                                             os.environ['POSTGRES_PASSWORD'], os.environ['POSTGRES_HOST'])
    logging.info('database connection ready')
    redis_client = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'],
                                     password=os.environ['REDIS_PASSWORD'], decode_responses=True)
    logging.info('redis connection is ready')
    searchEngine = Searcher(dbConnection, redis_client)

    app.run(host='0.0.0.0', port="8889")
