from __future__ import absolute_import, print_function
import flask
from textblob import Word
app = flask.Flask("__main__", static_folder="../frontend/build/static",
                  template_folder="../frontend/build")
from flask import Flask, request, jsonify
from flask import json, g
from flask_cors import CORS, cross_origin
import numpy as np
import requests
from pymongo import MongoClient
import dns
import re
import json


# Establish connection with MongoDB Atlas
client = MongoClient(
    "mongodb+srv://admin:admin@combining-hku7y.mongodb.net/test?retryWrites=true&w=majority")
db1 = client.foodfood
inverted_index_ff = db1.invertedindex.find()[0]
db2 = client.foodrepublic
inverted_index_fr = db2.invertedIndexfr.find()[0]
# return client
cors = CORS(app, resources={r"/results": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/results", methods=["POST"])
def results():
    try:
        allresult, mainresult = dataRetrieval(
            flask.request.get_data().decode("utf-8"))
        if type(mainresult) == 'str':
            mainresult = {
                "error": mainresult
            }
        return jsonify(mainresult)
    except:
        mainresult = {
            "error": "Sorry!, Too many chefs spoiled the recipe!"
        }
        print("Results not found")
        return jsonify(mainresult)
        


@app.route("/results", methods=["GET"])
def results_blank():
    try:
        return flask.redirect(flask.url_for('/'), code=200)
    except:
        print("Something went wrong!")


@app.route("/")
def index():
    try:
        return flask.redirect("http://sheeryachavan.github.io/searchengine", code=200)
    except:
        print("Something went wrong!")



# Retrieve recipes with the given input ingredients from the user
# Ranked results:(Explained with the help of example below)
# Suppose we have 3 ingredients as input.
# ranked_results_fffr will have 3 keys result0,result1,result2
# result0:recipes with ingredient1 in it
# result1:recipes with ingredient1 and ingredient2 in it
# result2:recipes with ingredient1,ingredient2 and ingredient3 in it
# final_result_fffr : contains the recipes with all the ingredients mentioned in the input 
def dataRetrieval(query):
    try:
        ingredients_str = query
        global inverted_index_ff
        global inverted_index_fr
        if re.search(r"\band\b", ingredients_str):
            ingredients_str = re.sub("and", "", ingredients_str)
        if re.search(r"\bor\b", ingredients_str):
            ingredients_str = re.sub("or", "", ingredients_str)
        ingredients_str = ingredients_str.split()
        stop_words = set(["salt", "pepper"])

        ingredients = [w for w in ingredients_str if not w in stop_words]


        # for foodfood
        individual_ing_ff = []
        ranked_results_ff = {}
        final_result_ff = []

        for (count, input_ingred) in enumerate(ingredients):
            ingred_combine_list_ff = []
            word2 = Word(input_ingred.lower())
            word1 = word2.lemmatize()
            singular_word_str = Word(word1).singularize()
            plural_word_str = Word(word1).pluralize()
            if singular_word_str in inverted_index_ff:
                ingred_combine_list_ff.extend(
                    inverted_index_ff[singular_word_str])
            if plural_word_str in inverted_index_ff:
                ingred_combine_list_ff.extend(
                    inverted_index_ff[plural_word_str])
            if input_ingred.lower() in inverted_index_ff:
                if not final_result_ff:
                    final_result_ff.extend(set(ingred_combine_list_ff))
                else:
                    final_result_ff = list(
                        set(final_result_ff) & set(ingred_combine_list_ff))
                if len(final_result_ff) > 0:
                    ranked_results_ff["result"+str(count)] = final_result_ff
        print(sorted(ranked_results_ff.keys()))
        finalff = ranked_results_ff[sorted(ranked_results_ff.keys())[-1]]
        final_result1_ff = getFinalResult(db1.reviews, finalff)

        # for food republic
        ranked_results_fr = {}
        final_result_fr = []
        # result = []

        for (count, input_ingred) in enumerate(ingredients):
            ingred_combine_list_fr = []
            word2 = Word(input_ingred.lower())
            word1 = word2.lemmatize()
            singular_word_str = Word(word1).singularize()
            plural_word_str = Word(word1).pluralize()
            if singular_word_str in inverted_index_fr:
                ingred_combine_list_fr.extend(
                    inverted_index_fr[singular_word_str])
            if plural_word_str in inverted_index_fr:
                ingred_combine_list_fr.extend(
                    inverted_index_fr[plural_word_str])
            if input_ingred.lower() in inverted_index_fr:
                if not final_result_fr:
                    final_result_fr.extend(set(ingred_combine_list_fr))
                else:
                    final_result_fr = list(set(final_result_fr) &
                                           set(ingred_combine_list_fr))
                if len(final_result_fr) > 0:
                    ranked_results_fr["result"+str(count)] = final_result_fr
        finalfr = ranked_results_fr[sorted(ranked_results_fr.keys())[-1]]
        final_result1_fr = getFinalResult(db2.fr_recipes, finalfr)
        final_result_fffr = final_result1_ff + final_result1_fr
        ranked_results_fffr = {}
        rslt_comb_list = []

        for result in ranked_results_ff:
            if result in ranked_results_fr:
                rslt_comb_list = ranked_results_ff[result] + \
                    ranked_results_fr[result]
                ranked_results_fffr[result] = rslt_comb_list

        print("=============================SP=======================")
        print(ranked_results_fffr)
        print("========================================================")
        print(final_result_fffr)
        return ranked_results_fffr, final_result_fffr
    except:
        print("Oops! Recipes not retrieved")
        return [], "Oops! Recipes not retrieved"

# Retrieve recipes respective to the id's from MongoDB Atlas
def getFinalResult(db, finalresult):
    try:
        final_result1 = []
        titlelist = []
        for recipe in finalresult:
            rec = db.find_one({"_id": recipe})
            rec.pop("_id", None)
            if rec["title"] not in titlelist:
                titlelist.append(rec["title"])
                final_result1.append(rec)
        return final_result1
    except:
        print("Recipes not found!")
        return []


app.run(host='0.0.0.0', port=80, debug=True)
