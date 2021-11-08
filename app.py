from flask import Flask, render_template, jsonify, request
from carrot_scrap import carrot_scrap
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbprac


@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/search', methods=['POST'])
# def search_word():
#     search_receive = request.form['search_give']
#     carrot_result = carrot_scrap(search_receive, 1)
#     return jsonify({'result': 'success'})


@app.route('/search', methods=['GET'])
def search():
    url_carrot_receive = request.args['search_give']
    carrot_result = carrot_scrap(url_carrot_receive, 1)
    return jsonify({'result': 'success', 'searching_info': carrot_result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
