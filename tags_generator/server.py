from flask import Flask
from flask import request
from flask import jsonify
import os

app = Flask(__name__)


import tags_generator.word2vec.query as word2vec_query

dump_path = os.getenv('MODEL_DUMP_PATH', 'tags_generator/word2vec/dumps/')
w2v_model, classifier, mlb = word2vec_query.load_model(dump_path)


@app.route("/api")
def hello_world():
    query = request.args.get('q', default="", type = str)
    if query == "":
        return "No query provided"

    tags = word2vec_query.suggest_tags(query, w2v_model, classifier, mlb)

    return jsonify(tags)
