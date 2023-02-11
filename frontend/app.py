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
 
    trinitclient.process_post(f'/api/signup',data)


    
    return redirect(f'/')


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
    return redirect(f'/')



if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0",port = PORT)