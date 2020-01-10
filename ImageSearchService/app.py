from flask import Flask, jsonify, request
import logging
from searcher import Searcher
from DB_controller import PostgresImageDBController
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
dbConnection = PostgresImageDBController("imagedb","searchservice","admin","localhost")
logging.info('database connection ready')
searchEngine = Searcher(dbConnection)

app = Flask(__name__)

@app.route('/search',methods=['GET'])
def search():
    if request.method == 'GET':
        content = request.get_json()
        out = searchEngine.search_keywords(content['tags'])
        return jsonify({'urls':out})

if __name__ == '__main__':
    app.run(port="8889")