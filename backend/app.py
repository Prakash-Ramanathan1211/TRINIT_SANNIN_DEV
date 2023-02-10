from math import prod
from time import pthread_getcpuclockid
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import random
import json
import pymongo
from pymongo import MongoClient
# import json
from bson import json_util
from datetime import date, datetime

cluster = MongoClient('mongodb+srv://prakash-1211:prakash@cluster0.enw9p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db = cluster["trinit"]

app  = Flask(__name__)

def get_last_user_id():
    col = db["user_details"]
    last_user_id      = col.find().sort([('user_id',-1)]).limit(1)

    try:
        last_user_id = last_user_id[0]['user_id']
    except:
        last_user_id = 0

    # user_id = last_user_id + 1

    return last_user_id

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    col = db["user_details"]
    email      = request.json['email']
    username   = request.json["username"]
    password   = request.json['password']
    address    = request.json['address']
    mobile     = request.json["mobile"]

    existing_user = col.find_one({"email": email})

    if existing_user:
        return "user already exist"
    
    user_id = get_last_user_id()

    new_user_id = user_id + 1
    
    curr_date = datetime.now()
    user_dict = {
        "user_id" : new_user_id,
        "username" : username,
        "email" : email,
        "password" : password,
        "address" : address,
        "mobile" : mobile,
        
        "created_at"   : curr_date,
        
    }

    col.insert_one(user_dict)

    result = {
        "result" : "Successfully signed up"

    }
    return json.dumps(result)


@app.route('/get/questions', methods=['GET'])
def get_questions():
    col = db["question_details"]
    question_details = col.find()

    question_details_list = []

    for question_detail in question_details:

        question_id = question_detail["question_id"]
        question_title = question_detail["question_title"]
        question_description = question_detail["question_description"]
        upvotes = question_detail["upvotes"]
        downvotes = question_detail["downvotes"]
        view_count = question_detail["view_count"]
        questioned_by = question_detail["questioned_by"]
        created_at = question_detail["created_at"]
        updated_at = question_detail["updated_at"]

        question_details_dict = {
            "question_id" : question_id,
            "question_title" : question_title,
            "question_description" : question_description,
            "upvotes"  : upvotes,
            "downvotes" : downvotes,
            "view_count"  : view_count,
            "questioned_by"  : questioned_by,
            "created_at"  : created_at,
            "updated_at"  : updated_at
        }

        question_details_list.append(question_details_dict)
    
    result = {
        "result" : question_details_list
    }

    return json.dump(result)


def get_last_question_id():
    col = db["question_details"]
    last_user_id      = col.find().sort([('question_id',-1)]).limit(1)

    try:
        last_user_id = last_user_id[0]['question_id']
    except:
        last_user_id = 0

    # user_id = last_user_id + 1

    return last_user_id

@app.route('/add/questions', methods=['POST'])
def add_questions():
    
    col = db["question_details"]

    questioned_by = request.json("questioned_by")
    question_title = request.json("question_title")
    question_description = request.json("question_description")
    upvotes = 0
    downvotes = 0
    view_count = 0

    question_id = get_last_question_id() 

    new_question_id = question_id+1

    curr_date = datetime.now()

    add_question_dict = {
        "question_id" : new_question_id,
        "questioned_by" : questioned_by,
        "question_title" : question_title,
        "question_description" : question_description,
        "upvotes" : upvotes,
        "downvotes" : downvotes,
        "view_count" : view_count,
        "created_at": curr_date,
        "updated_at" : curr_date
    } 


    col.insert_one(add_question_dict)

    result = {
        "result" : "successfully added"
    }

    return json.dumps(result)
























if __name__== "__main__":
    app.run(host="0.0.0.0", debug = True,port = 5003)

