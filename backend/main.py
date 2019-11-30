from __future__ import absolute_import, print_function
import flask
app = flask.Flask("__main__", static_folder="../findit/build/static", template_folder="../findit/build")
from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask import json, g
from flask_cors import CORS
import numpy as np
import spacy
import requests
import en_core_web_lg
result1 = {
    "hello":"how are",
    "khana":"kha ke jana"
}
nlp = en_core_web_lg.load()
@app.route("/results",methods = ["GET"])
def results():
    print(flask.request.data)
    return json_response(result1)
@app.route("/")
def index():
    query = flask.request.args.get("query",None)
    print("hi"+str(flask.request.args))
    print(flask.request.args)
    if query:
        app.logger.info("Query {} received".format(query))
        # results = retrieve(query)
        return flask.redirect(flask.url_for('results'),code=200)
    return json_response(result1)
    

app.run(debug = True)