from textblob import Word

def dataRetrieval(query):
    ingredients_str = query
    ingredients_str = ingredients_str.split()
    stop_words = set(["salt","pepper"]) 


    ingredients = [w for w in ingredients_str if not w in stop_words] 
    print(ingredients)
    
    # ingredients = ["tomato","Carrot","cabbage"]
    ranked_results = {}
    final_result = []
    result = []
    inverted_index = db.invertedindex[0]
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
                final_result = list(set(final_result) & set(ingred_combine_list))
    #             print(final_result)
            
            ranked_results["result"+str(count)] = final_result
    #         print(ranked_results)
    #         print("======================================================================================")
            
   
    return ranked_results,final_result

