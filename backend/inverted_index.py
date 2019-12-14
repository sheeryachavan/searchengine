from pymongo import MongoClient
import dns
client = MongoClient("mongodb+srv://admin:admin@combining-hku7y.mongodb.net/test?retryWrites=true&w=majority")
db = client.foodfood

inverted_index ={}
docs=[]
with client:
    
    recipes = db.reviews.find()
    
    for recipe in recipes:
        for ingred in recipe["key_ing"]:

            ingredient_wordlist = ingred.split()
            ingredient_wordlist = [word.lower() for word in ingredient_wordlist]
            ingredient_wordlist = list(set(ingredient_wordlist))

            for ingred1 in ingredient_wordlist:

                if ingred1 not in inverted_index:
                    inverted_index[ingred1] = []
                inverted_index[ingred1].append(recipe["title"])
            docs.append(" ".join(ingred))

print(inverted_index)
    # return inverted_index