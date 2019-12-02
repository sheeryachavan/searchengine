from __future__ import absolute_import, print_function
import flask
from textblob import Word
app = flask.Flask("__main__", static_folder="../frontend/build/static",
                  template_folder="../frontend/build")
from flask import Flask, request, jsonify
# from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask import json, g
from flask_cors import CORS, cross_origin
import numpy as np
import requests
from pymongo import MongoClient
import dns

# def MongoConnection(): 
client = MongoClient("mongodb+srv://admin:admin@combining-hku7y.mongodb.net/test?retryWrites=true&w=majority")
    # return client
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

import json


@app.route("/results", methods=["POST"])
def results():
    print("hello")
    print(flask.request.url)
    print(flask.request.get_data().decode("utf-8"))
    # print(flask.request.data.decode("utf-8"))
    allresult,mainresult = dataRetrieval(flask.request.get_data().decode("utf-8"))
    # print(query)
    return jsonify(mainresult)
@app.route("/results", methods=["GET"])
def results_blank():
    return flask.redirect(flask.url_for('/'), code=200)


@app.route("/")
def index():
    
    return flask.redirect("http://sheeryachavan.github.io/searchengine", code=200)


def dataRetrieval(query):
    ingredients_str = query
    print(query)
    ingredients_str = ingredients_str.split()
    stop_words = set(["salt", "pepper"])
    db = client.foodfood
    ingredients = [w for w in ingredients_str if not w in stop_words]
    print(ingredients)
    inverted_index = db.invertedindex.find()[0]
    # ingredients = ["tomato","Carrot","cabbage"]
    ranked_results = {}
    final_result = []
    result = []

    for (count, input_ingred) in enumerate(ingredients):
        #     print(count)
        ingred_combine_list = []
        word2 = Word(input_ingred.lower())
        word1 = word2.lemmatize()
        singular_word_str = Word(word1).singularize()
        plural_word_str = Word(word1).pluralize()
        if singular_word_str in inverted_index:
            ingred_combine_list.extend(inverted_index[singular_word_str])
        if plural_word_str in inverted_index:
            ingred_combine_list.extend(inverted_index[plural_word_str])
        if input_ingred.lower() in inverted_index:
            if not final_result:
                final_result.extend(set(ingred_combine_list))
            else:
                final_result = list(set(final_result) &
                                    set(ingred_combine_list))
                print(final_result)

            ranked_results["result"+str(count)] = final_result
    #         print(ranked_results)
    #         print("======================================================================================")
    # print("====================================================")
    # print(final_result)
    # print("========================================================")
    final_result1 = []
    titlelist = []
    for recipe in final_result:
        
        rec = db.reviews.find_one({"_id":recipe})
        rec.pop("_id",None)
        if rec["title"] not in titlelist:
            titlelist.append(rec["title"])
            final_result1.append(rec)


    print("=============================SP=======================")
    # print(set(final_result1))
    print("========================================================")
    return ranked_results, final_result1


# app.run(host='127.0.0.1',port='5000',debug=True)
