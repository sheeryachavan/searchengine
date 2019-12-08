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
import re
import json


# def MongoConnection(): 
client = MongoClient("mongodb+srv://admin:admin@combining-hku7y.mongodb.net/test?retryWrites=true&w=majority")
    # return client
cors = CORS(app, resources={r"/results": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'



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
    
    if re.search(r"\band\b",ingredients_str):
        ingredients_str = re.sub("and","",ingredients_str)
    if re.search(r"\bor\b",ingredients_str):
        ingredients_str = re.sub("or","",ingredients_str)
    # if re.search(r"\,",ingredients_str):
    #     ingredients_str = re.sub(",","",ingredients_str)

    ingredients_str = ingredients_str.split()
    stop_words = set(["salt", "pepper"])
    
    ingredients = [w for w in ingredients_str if not w in stop_words]
    print(ingredients)

    # for foodfood
    db1 = client.foodfood
    inverted_index_ff = db1.invertedindex.find()[0]
    # ingredients = ["tomato","Carrot","cabbage"]
    individual_ing_ff = []
    ranked_results_ff = {}
    final_result_ff = []
    # result = []

    for (count, input_ingred) in enumerate(ingredients):
        #     print(count)
        ingred_combine_list_ff = []
        word2 = Word(input_ingred.lower())
        word1 = word2.lemmatize()
        singular_word_str = Word(word1).singularize()
        plural_word_str = Word(word1).pluralize()
        if singular_word_str in inverted_index_ff:
            ingred_combine_list_ff.extend(inverted_index_ff[singular_word_str])
        if plural_word_str in inverted_index_ff:
            ingred_combine_list_ff.extend(inverted_index_ff[plural_word_str])
        if input_ingred.lower() in inverted_index_ff:
            if not final_result_ff:
                final_result_ff.extend(set(ingred_combine_list_ff))
            else:
                final_result_ff = list(set(final_result_ff) &
                                    set(ingred_combine_list_ff))
                print(final_result_ff)

            ranked_results_ff["result"+str(count)] = final_result_ff

    final_result1_ff = []
    titlelist_ff = []
    for recipe in final_result_ff:
        
        rec = db1.reviews.find_one({"_id":recipe})
        rec.pop("_id",None)
        if rec["title"] not in titlelist_ff:
            titlelist_ff.append(rec["title"])
            final_result1_ff.append(rec)


    # for food republic
    db2 = client.foodrepublic
    inverted_index_fr = db2.invertedIndexfr.find()[0]
    # ingredients = ["tomato","Carrot","cabbage"]
    ranked_results_fr = {}
    final_result_fr = []
    # result = []

    for (count, input_ingred) in enumerate(ingredients):
        #     print(count)
        ingred_combine_list_fr = []
        word2 = Word(input_ingred.lower())
        word1 = word2.lemmatize()
        singular_word_str = Word(word1).singularize()
        plural_word_str = Word(word1).pluralize()
        if singular_word_str in inverted_index_fr:
            ingred_combine_list_fr.extend(inverted_index_fr[singular_word_str])
        if plural_word_str in inverted_index_fr:
            ingred_combine_list_fr.extend(inverted_index_fr[plural_word_str])
        if input_ingred.lower() in inverted_index_fr:
            if not final_result_fr:
                final_result_fr.extend(set(ingred_combine_list_fr))
            else:
                final_result_fr = list(set(final_result_fr) &
                                    set(ingred_combine_list_fr))
                print(final_result_fr)

            ranked_results_fr["result"+str(count)] = final_result_fr

    final_result1_fr = []
    titlelist_fr = []
    for recipe in final_result_fr:
        
        rec = db2.fr_recipes.find_one({"_id":recipe})
        rec.pop("_id",None)
        if rec["title"] not in titlelist_fr:
            titlelist_fr.append(rec["title"])
            final_result1_fr.append(rec)





    final_result_fffr = final_result1_ff + final_result1_fr
    ranked_results_fffr = {}
    rslt_comb_list = []

    for result in ranked_results_ff:
        print(result)
        if result in ranked_results_fr:
            rslt_comb_list = ranked_results_ff[result] + ranked_results_fr[result]
            ranked_results_fffr[result] = rslt_comb_list

    print("=============================SP=======================")
    print(ranked_results_fffr)
    print("========================================================")
    print(final_result_fffr)
    print("=======================================")
    return ranked_results_fffr, final_result_fffr
    


app.run(host='127.0.0.1',port='5000',debug=True)
