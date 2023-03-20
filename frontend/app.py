import re
from flask import Flask,render_template, jsonify, request, url_for, redirect
import random
import json

# import json
from bson import json_util
from consumer import TrinitClient

import os
from werkzeug.utils import secure_filename
from datetime import datetime



app  = Flask(__name__)
PORT = 3000

trinitclient = TrinitClient()




@app.route("/", methods=["GET"])
def startpy():

    return render_template("login2.html") 

# @app.route("/login", methods=["POST"])
# def post_login():

#     email = request.values.get('email')
#     password = request.values.get('password')

#     data = {
#         "email" : email,
#         "password"  : password 
#     }

#     result  = trinitclient.process_post('/login', data)


@app.route("/signup", methods=["GET"])
def signup():
    return render_template("login.html") 

@app.route("/signup", methods=["GET","POST"])
def post_signup():

    email = request.values.get('email')
    username = email 
    password = request.values.get('password')
    usertype = request.values.get('usertype')
    location = request.values.get('address')
    mobile   = request.values.get('mobile')
 
    data = {
        "email" : email,
        "username" : username,
        "password" : password,
        "usertype" : usertype,
        "address"  : location,
        "mobile"   : mobile
    }

    # print(data) 
 
    trinitclient.process_post('/api/signup',data)


    
    return "successfully signed up"


@app.route("/login", methods=["POST"])
def post_login():

    email = request.values.get('email')
    password = request.values.get('password')

    data = {
        "email" : email,
        "password"  : password 
    }
    result  = trinitclient.process_post('/api/login', data)

    user_id = result["user_id"]

    print("****************",user_id)
    return "successfully logged in"

'''
[{'created_at': 'Fri, 10 Feb 2023 00:00:00 GMT', 'downvotes': 100, 
'question_description': 'hehe', 'question_id': 1, 'question_tag': 'rice',
 'question_title': 'what is what', 'questioned_by': 1,
  'updated_at': 'Fri, 10 Feb 2023 00:00:00 GMT', 
  'upvotes': 200, 'view_count': 1000}]

'''
@app.route("/discussion/forum/<user_id>", methods=["GET"])
def discussion_forum(user_id):

    questions = trinitclient.process_get('/get/questions')

    print(questions["result"])

    return render_template("qna.html", questions = questions["result"]) 

'''
[{'answer_description': 'this is the answer', 'answer_id': 1, 'answered_by': 2, 
'created_at': 'Fri, 10 Feb 2023 23:43:35 GMT', 'downvotes': 100, 
'question_description': 'Does scarifying avocadoes before putting them in water or a ziplock bag decrease the germination time? And if so, why is it extremely rare to see this procedure mentioned?', '
question_id': 1, 'question_tag': 'rice', 
'question_title': 'Scarifying / cutting top and bottom of avocado seeds for faster germination? Also in water?', 
'questioned_by': 1, 'updated_at': 'Fri, 10 Feb 2023 23:43:35 GMT', 'upvotes': 200}]

'''

@app.route("/discussion/forum/question/<question_id>/<user_id>", methods=["GET"])
def discussion_forum_single(question_id,user_id):
    # user_id = user_id
    question_id = int(question_id)

    url = f'/get/answers/{question_id}'

    questions = trinitclient.process_get(url)

    print(questions["result"])
    length = len(questions["result"])

    return render_template("qna-single.html", questions = questions["result"],length = length,question_id = question_id,user_id = user_id)

@app.route("/add/answer/<question_id>/<user_id>", methods=["POST"])
def add_answer(question_id, user_id):

    answer_description = request.values.get('answer_description')
    
    data = {
        "answer_description" : answer_description,
        "question_id"        : question_id,
        "answered_by"            : user_id
    }

    url = "/add/answer"

    result = trinitclient.process_post(url, data)

    return redirect(f"/discussion/forum/question/{question_id}/{user_id}")

@app.route("/scheme/recommendation", methods=["GET"])
def scheme_recommendation():

    

    return render_template("scheme.html")


if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0",port = PORT)