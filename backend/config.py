
from pymongo import MongoClient
import dns

def MongoConnection(): 
    client = MongoClient("mongodb+srv://admin:admin@combining-hku7y.mongodb.net/test?retryWrites=true&w=majority")
    return client