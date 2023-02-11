from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import random
import json
import pymongo
from pymongo import MongoClient
# import json
from bson import json_util
from datetime import date, datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

cluster = MongoClient('mongodb+srv://prakash-1211:prakash@cluster0.enw9p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db = cluster["trinit"]

def create_question_details():
    col = db["question_details"]
    
    current_datetime = datetime.now()

    current_datetime = datetime.now()
    formatted_date = datetime(current_datetime.year, current_datetime.month, current_datetime.day-1)
  
    discussion_entry_dict = {
        "question_id"    : 1,
        "questioned_by"        : 1,
        "question_title"     : "what is what",
        "question_tag"       : "rice",
        "question_description": "hehe",
        "upvotes"          : 200,
        "downvotes"      : 100,
        "view_count"       : 1000,
 
        "created_at"     : current_datetime,
        "updated_at"       : current_datetime
        
    }

    try:
        x = col.insert_one(discussion_entry_dict)
        print(x)
        return True

    except:
        # print(e)
        print('Duplicate Error')

        return False

def create_answer_details():
    col = db["answer_details"]
    
    current_datetime = datetime.now()

    current_datetime = datetime.now()
    formatted_date = datetime(current_datetime.year, current_datetime.month, current_datetime.day-1)
  
    discussion_entry_dict = {
        "answer_id"    : 1,
        "question_id"     : 1,

        "answer_description": "this is the answer",
        "answered_by"     : 2,
        "upvotes"          : 200,
        "downvotes"      : 100,
  
 
        "created_at"     : current_datetime,
        "updated_at"       : current_datetime
        
    }

    try:
        x = col.insert_one(discussion_entry_dict)
        print(x)
        return True

    except:
        # print(e)
        print('Duplicate Error')

        return False

def hash_password(password):

    return bcrypt.generate_password_hash(password)

def create_user_details():

    col = db["user_details"]
    current_datetime = datetime.now()

    password = hash_password("prakash1211")

    user_entry_dict = {
        "user_id"    : 1,
        "username"     : "mohith",

        "password":    password,
        "usertype"     : "farmer",
        "location"          : "Chennai",
        "emailid"      : "prashprakash1211@gmail.com",
        "mobile"       : 9810430540,
 
        "created_at"     : current_datetime,
        "updated_at"       : current_datetime
        
    }

    try:
        x = col.insert_one(user_entry_dict)
        print(x)
        return True

    except:
        # print(e)
        print('Duplicate Error')

        return False
    


def startpy():

    # create_question_details() 
    # create_product_details()
    # create_sales()
    # create_answer_details()
    create_user_details()

if __name__ == '__main__':
    startpy()