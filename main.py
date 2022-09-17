import pymongo
from datetime import datetime as dt
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from validator_schema import book_validator, author_validator
import pprint

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")

conection_string = F"mongodb+srv://lucin21:{password}@tutorial.okcdgcc.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(conection_string)
dbs = client.list_database_names()
test_db = client["test"]
collection = test_db.list_collection_names()
# print(collection)
# print(dbs)


def insert_one_doc():
    collection = test_db.test
    test_document = {
        "name":"Lucin",
        "type":"test"
    }
    inserted_id = collection.insert_one(test_document).inserted_id
    print(inserted_id)

# insert_one_doc()

production = client["production"] #se conecta o crea la base de datos
person_collection = production["person_collection"] # se conecta o crea la coleccion

def create_document():
    names = ["Mnauel", "Lujan", "Aliria"]
    last_names = ["Teras", "Vasquez", "Gutierrez"]
    ages = [10, 13, 15]
    docs = []

    for name, last_name, age in zip(names,last_names,ages):
        doc = {"name":name, "last_name":last_name, "age":age}
        docs.append(doc)

    person_collection.insert_many(docs)

# create_document()

def find_all_people():
    peoples = person_collection.find()
    for people in peoples:
        print(people)

# find_all_people()

def find_lucin():
    lucin = person_collection.find_one({"name": "lucin"})
    print(lucin)

# find_lucin()


def count_all_people():
    count = person_collection.count_documents(filter={})
    print(count)
# count_all_people()


def get_person_by_id(person_id):
    _id = ObjectId(person_id)
    person = person_collection.find_one({"_id":_id})
    print(person)

# get_person_by_id("6324e19862b7b8879b8fa134")

def get_age_range(min_age,max_age):
    query = {"$and":[
        {"age":{"$gte":min_age}},
        {"age": {"$lte": max_age}}
    ]
    }
    people = person_collection.find(query).sort("age")
    for person in people:
        print(person)

# get_age_range(9,18)

def some_colums():
    colums = {"_id":0, "name":1}
    people = person_collection.find({}, colums)
    for person in people:
        print(person)

# some_colums()

def update_one(id_person):
    _id = ObjectId(id_person)

    all_update = {
        # "$set":{"new_filed":True},
        # "$inc":{"age":50},
        "$rename":{"nombre":"name","apellido":"last_name"}
    }
    # person_collection.update_one({"_id": _id}, all_update)
    person_collection.update_one({"_id": _id}, {"$unset": {"new_filed":""}})
# update_one("6324e19862b7b8879b8fa134")

def replace_one(id_person):
    _id = ObjectId(id_person)
    new_doc = {
        "name":"test",
        "last_name": "test",
        "age": 27
    }
    person_collection.replace_one({"_id":_id}, new_doc)

# replace_one("6324e19862b7b8879b8fa134")

def delete_by_id(person_id):
    _id = ObjectId(person_id)
    person_collection.delete_one({"_id":_id})

# delete_by_id("6324e19862b7b8879b8fa134")

address = {
    "_id": "5324e19862b7b8879b8fa135",
    "street":"calle colombia",
    "zip":7001,
    "country":"venezuela",
    "city":"san fernando"
}


def add_address_embed(person_id, address):
    _id = ObjectId(person_id)

    person_collection.update_one({"_id":_id}, {"$addToSet": {"addresses": address}})

# add_address_embed("6324e19862b7b8879b8fa135", address)

def address_relationship(person_id, address):
    _id = ObjectId(person_id)
    address = address.copy()
    address["onwer_id"] = person_id
    address_collection = production["address"]
    address_collection.insert_one(address)

# address_relationship("6324f0ab27f697f341a7c8f9", address)

# try:
#     production.create_collection("book")
# except Exception as e:
#     print(e)
#
# production.command("collMod", "book", validator=book_validator)
#
# try:
#     production.create_collection("author")
# except Exception as e:
#     print(e)
#
# production.command("collMod", "author", validator=author_validator)

def create_data():
    authors = [
        {"first_name": "Pablo",
         "last_name": "Neruda",
         "date_of_bird": dt(1940, 5, 25)},
        {"first_name": "Daniel",
         "last_name": "Orozco",
         "date_of_bird": dt(1970, 1, 25)},
        {"first_name": "Pedro",
         "last_name": "Tirado",
         "date_of_bird": dt(1990, 1, 12)},
        {"first_name": "bulma",
         "last_name": "capsula",
         "date_of_bird": dt(1400, 3, 12)},
        {"first_name": "goku",
         "last_name": "gonzalez",
         "date_of_bird": dt(1850, 11, 12)},
    ]
    author_collection = production["author"]
    authors = author_collection.insert_many(authors).inserted_ids
    books = [{
        "title": "MongoDB advanced tutorial",
        "author": [authors[0]],
        "publish_date": dt.today(),
        "type": "Non-Ficcion",
        "copies": 5
        },
    {
        "title": "MongoDB advanced tutorial",
        "author": [authors[1]],
        "publish_date": dt(1850, 11, 12),
        "type": "Non-Ficcion",
        "copies": 5
        },
    {
        "title": "una hisotria de soledad",
        "author": [authors[2]],
        "publish_date": dt(1400, 3, 12),
        "type": "Ficcion",
        "copies": 5
        },
    {
        "title": "Petardos",
        "author": [authors[3]],
        "publish_date": dt(1970, 1, 25),
        "type": "Ficcion",
        "copies": 5
        },
    {
        "title": "Django",
        "author": [authors[4]],
        "publish_date": dt.today(),
        "type": "Non-Ficcion",
        "copies": 5
        },

    {
        "title": "Python",
        "author": [authors[3]],
        "publish_date": dt.today(),
        "type": "Non-Ficcion",
        "copies": 5
        }

    ]

    book_collection = production.book
    book_collection.insert_many(books)
# create_data()

# books_containing_p = production.book.find({"title":{"$regex": "P{1}"}})
#
# print(list(books_containing_p))

authors_and_books = production["author"].aggregate([{
    "$lookup":{
        "from": "book",
        "localField": "_id",
        "foreignField": "author",
        "as": "books"
    }
}])

# print(list(authors_and_books))

authors_and_books_count = production["author"].aggregate([{
    "$lookup":{
        "from": "book",
        "localField": "_id",
        "foreignField": "author",
        "as": "books"
    }
},
    {"$addFields": {
     "total_books":{"$size":"$books"}
    }},
    {"$project":{"firts_name": 1, "last_name": 1, "total_books": 1, "_id": 0}}
])

# print(list(authors_and_books_count))

books_with_old_author = production["book"].aggregate([{
    "$lookup":
        {"from": "author",
         "localField": "author",
         "foreignField": "_id",
         "as": "authors"}
},
    {"$set":{
        "authors":{"$map":{
            "input": "$authors",
            "in":{
                "age":{
                    "$dateDiff":{
                        "startDate": "$$this.date_of_bird",
                        "endDate": "$$NOW",
                        "unit": "year"
                    }
                },
                "first_name": "$$this.first_name",
                "last_name": "$$this.last_name",
            }
        }}
    }},
    {"$match":{
        "$and": [
            {"authors.age": {"$gte": 50}},
            {"authors.age": {"$lte": 150}},

        ]

    }},
    {
        "$sort":{
            "age":1
        }
    }
])

# print(list(books_with_old_author))
import pyarrow
from pymongoarrow.api import Schema
from pymongoarrow.monkey import patch_all
import pymongoarrow as pma

patch_all()

author = Schema({"_id": ObjectId, "first_name": pyarrow.string(), "last_name": pyarrow.string(), "date_of_bird":dt})
df = production["author"].find_pandas_all({}, schema=author)

print(df)

