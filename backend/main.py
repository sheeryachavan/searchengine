from __future__ import absolute_import, print_function
import flask
app = flask.Flask("__main__", static_folder="../frontend/build/static",
                  template_folder="../frontend/build")
from flask import Flask, request, jsonify
# from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask import json, g
from flask_cors import CORS, cross_origin
import numpy as np
import spacy
import requests
import en_core_web_lg
cors = CORS(app, resources={r"/results": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
result1 = [
    {
        "_id": "5ddc406b1ced558962a44904",
        "image": "http://fd2static.foodfood.com.s3.ap-south-1.amazonaws.com/images/Chicken-Farcha-84589.jpg",
        "title": "Chicken Farcha",
        "Prep": " 2 hours",
        "Cook": " 30 minutes",
        "key_ing": ["Chicken drumsticks", "Eggs", "Breadcrumbs"],
        "desc": "A popular Parsi deep-fried chicken drumsticks ",
        "link": "https://www.foodfood.com/recipedetails/chicken-farcha"
    },
    {
        "_id": "5ddc406b1ced558962a44904",
        "image": "http://fd2static.foodfood.com.s3.ap-south-1.amazonaws.com/images/Khatti-Mooli-2948.jpg",
        "title": "Chicken Farcha",
        "Prep": " 2 hours",
        "Cook": " 30 minutes",
        "key_ing": ["Chicken drumsticks", "Eggs", "Breadcrumbs"],
        "desc": "A popular Parsi deep-fried chicken drumsticks ",
        "link": "https://www.foodfood.com/recipedetails/chicken-farcha"
    },
    {
        "_id": "5ddc406b1ced558962a44904",
        "image": "http://fd2static.foodfood.com.s3.ap-south-1.amazonaws.com/images/Chicken-Farcha-84589.jpg",
        "title": "Chicken Farcha",
        "Prep": " 2 hours",
        "Cook": " 30 minutes",
        "key_ing": ["Chicken drumsticks", "Eggs", "Breadcrumbs"],
        "desc": "A popular Parsi deep-fried chicken drumsticks ",
        "link": "https://www.foodfood.com/recipedetails/chicken-farcha"
    },
    {
        "_id": "5ddc406b1ced558962a44904",
        "image": "http://fd2static.foodfood.com.s3.ap-south-1.amazonaws.com/images/Khatti-Mooli-2948.jpg",
        "title": "Chicken Farcha",
        "Prep": " 2 hours",
        "Cook": " 30 minutes",
        "key_ing": ["Chicken drumsticks", "Eggs", "Breadcrumbs"],
        "desc": "A popular Parsi deep-fried chicken drumsticks ",
        "link": "https://www.foodfood.com/recipedetails/chicken-farcha"
    },
    {
        "_id": "5ddc406b1ced558962a44904",
        "image": "http://fd2static.foodfood.com.s3.ap-south-1.amazonaws.com/images/Chicken-Farcha-84589.jpg",
        "title": "Chicken Farcha",
        "Prep": " 2 hours",
        "Cook": " 30 minutes",
        "key_ing": ["Chicken drumsticks", "Eggs", "Breadcrumbs"],
        "desc": "A popular Parsi deep-fried chicken drumsticks ",
        "link": "https://www.foodfood.com/recipedetails/chicken-farcha"
    }
]
nlp = en_core_web_lg.load()
import json

@app.route("/results", methods=["POST"])
def results():
    print("hello")
    print(flask.request.url)
    print(flask.request.data.decode('utf-8'))
    # print(query)
    return jsonify(result1)


@app.route("/")
def index():
    query = flask.request.args.get("query", None)
    print("hi"+str(flask.request.args))
    print(flask.request.args)
    if query:
        app.logger.info("Query {} received".format(query))
        # results = retrieve(query)
        return flask.redirect(flask.url_for('results'), code=200)
    return flask.redirect(flask.url_for('/'), code=200)


app.run(debug=True)
