from math import prod
import re
from time import pthread_getcpuclockid
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
        question_tag = question_detail["question_tag"]
        created_at = question_detail["created_at"]
        updated_at = question_detail["updated_at"]

        question_details_dict = {
            "question_id" : question_id,
            "question_title" : question_title,
            "question_description" : question_description,
            "upvotes"  : upvotes,
            "downvotes" : downvotes,
            "view_count"  : view_count,
            "question_tag"  : question_tag,
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
    question_tag = request.json('question_tag')
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
        "question_tag"  : question_tag,
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

def get_last_answer_id():
    col = db["answer_details"]
    last_user_id      = col.find().sort([('answer_id',-1)]).limit(1)

    try:
        last_user_id = last_user_id[0]['answer_id']
    except:
        last_user_id = 0

    # user_id = last_user_id + 1

    return last_user_id

@app.route('/add/answer', methods=['POST'])
def add_answer():

    col = db["answer_details"]

    question_id = request.json("question_id")
    answer_description = request.json("answer_description")
    answered_by = request.json("answered_by")
    upvotes  = 0
    downvotes = 0

    answer_id = get_last_answer_id()

    new_answer_id = answer_id + 1

    curr_date = datetime.now()

    add_answer_dict = {
        "answer_id" : new_answer_id,
        "question_id" : question_id,
        "answer_description" : answer_description,
        "answered_by" : answered_by,
        "upvotes" : upvotes,
        "downvotes" : downvotes,

        "created_at": curr_date,
        "updated_at" : curr_date
    } 

    col.insert_one(add_answer_dict)

    result = {
        "result" : "successfully added"
    }

    return json.dumps(result)


@app.route('/get/answers/<question_id>', methods=['GET'])
def get_answers(question_id):
    col = db["answer_details"]

    col2 = db["question_details"]
    answer_details = col.find({"question_id":int(question_id)})

    answer_details_list = []

    for answer_detail in answer_details:

        answer_id = answer_detail["answer_id"]
        answer_description = answer_detail["answer_description"]
        answered_by = answer_detail["answered_by"]
        question_id = answer_detail["question_id"]

        question_details = col2.find_one({"question_id": int(question_id)})

        questioned_by = question_details["questioned_by"]
        question_title = question_details["question_title"]
        question_description = question_details["question_description"]
        question_tag  = question_details["question_tag"]

        upvotes = answer_detail["upvotes"]
        downvotes = answer_detail["downvotes"]

        created_at = answer_detail["created_at"]
        updated_at = answer_detail["updated_at"]

        answer_details_dict = {
            "answer_id" : answer_id,
            "answer_description" : answer_description,
            "answered_by"   : answered_by,

            "question_id" : question_id,
            "question_title" : question_title,
            "question_description" : question_description,
            "question_tag" : question_tag,
            "upvotes"  : upvotes,
            "downvotes" : downvotes,

            "questioned_by"  : questioned_by,
            "created_at"  : created_at,
            "updated_at"  : updated_at
        }

        answer_details_list.append(answer_details_dict)
    
    result = {
        "result" : answer_details_list
    }

    return json.dump(result)

@app.route('/get/filtered/questions', methods=['GET','POST'])
def get_filtered_questions():

    col = db["question_details"]

    question_tag = request.json()

    question_details_list = []

    question_details = col.find({'question_tag':question_tag})

    for question_detail in question_details:
        question_id = question_detail["question_id"]
        question_title = question_detail["question_title"]
        question_description = question_detail["question_description"]
        upvotes = question_detail["upvotes"]
        downvotes = question_detail["downvotes"]
        view_count = question_detail["view_count"]
        questioned_by = question_detail["questioned_by"]
        question_tag = question_detail["question_tag"]
        created_at = question_detail["created_at"]
        updated_at = question_detail["updated_at"]

        question_details_dict = {
            "question_id" : question_id,
            "question_title" : question_title,
            "question_description" : question_description,
            "upvotes"  : upvotes,
            "downvotes" : downvotes,
            "view_count"  : view_count,
            "question_tag"  : question_tag,
            "questioned_by"  : questioned_by,
            "created_at"  : created_at,
            "updated_at"  : updated_at
        }

        question_details_list.append(question_details_dict)
    
    result = {
        "result" : question_details_list
    }

    return json.dump(result)

def hash_password(password):

    return bcrypt.generate_password_hash(password)

@app.route('/api/signup', methods=['POST'])
def api_signup():

    col = db["user_details"]

    user_id  = get_last_user_id()
    new_user_id = user_id + 1
    username = request.json("username")
    password = request.json("password")
    hashed_password = hash_password(password)
    usertype  = request.json("usertype")
    location = request.json("location")
    emailid  = request.json("emailid")
    mobile   = request.json("mobile")


    curr_date = datetime.now()

    add_user_dict = {
        "user_id" : new_user_id,
        "username" : username,
        "password" : hashed_password,
        "usertype" : usertype,
        "location" : location,
        "emailid" : emailid,
        "mobile"  : mobile,
        "created_at": curr_date,
        "updated_at" : curr_date
    } 

    col.insert_one(add_user_dict)

    result = {
        "result" : "successfully added"
    }

    return json.dumps(result)

def match_password(db_password, password):

    return bcrypt.check_password_hash(db_password, password)

@app.route('/api/login' , methods = ["GET"])
def api_login():

    col = db["user_details"]
    username      = request.json['username']
    password   = request.json['password']

    user_creds = col.find_one({"username" : username})

    if (user_creds is None):
        return "user not found"

    if (not match_password(user_creds['password'], password)):
        return "invalid creds"

    user_id = user_creds["user_id"]
    email = user_creds["email"]
    location = user_creds["location"]

    result_dict = {
        "user_id" : user_id,
        "email" : email,
        "location" : location,
       
    }

    return json.dumps(result_dict)
    
    
if __name__== "__main__":
    app.run(host="0.0.0.0", debug = True,port = 5003)

