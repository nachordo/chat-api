from api.app import app
from flask import request, send_from_directory
from db.sqlConnection import get_table,insert_chat
from bson import json_util
import os
from random import choice

# Decorators
@app.route("/")
def hello_world():
    return {"hello": "World!"}

@app.route("/help")
def help():
    return {"welcome":"Welcome to my API"}

@app.route("/test")
def testing():
    name = request.args.get("name")
    other = request.args.get("other")
    return {"name":name, "other":other}



@app.route("/sql/<name>")
def sql(name):
    return json_util.dumps(list(get_table(name)))

@app.route("/chat/create/<name>")
def chat_create(name):
    members = request.args.get("members")
    lst = list(map(int, members))
    #needs to add people to the chat
    # results = list(map(int, results))
    return insert_chat(name,lst)

@app.route("/user/create/<name>")
def user_create(name):
    return {"not":"today"}

@app.route("/chat/adduser/<name>")
def chat_adduser(name):
    return {"not":"today"}

@app.route("/chat/addmessage/<name>")
def add_mensage(name):
    return {"not":"today"}

@app.route("/chat/list/<name>")
def mess_from_chat(name):
    return {"not":"today"}

@app.route("/chat/sentiment/<name>")
def sent_from_chat(name):
    return {"not":"today"}

#app.run()
