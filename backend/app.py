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





















if __name__== "__main__":
    app.run(host="0.0.0.0", debug = True,port = 5003)

