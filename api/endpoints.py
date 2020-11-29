from api.app import app
from flask import request, send_from_directory
from db.sqlConnection import *
from sentimet.sentiment_functions import obtain_sentiment
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




@app.route("/chat/create/<name>")
def chat_create(name):
    members = request.args.get("members")
    members=members.split(",")
    lst = list(map(int, members))
    #needs to add people to the chat
    # results = list(map(int, results))
    return insert_chat(name,lst)

@app.route("/user/create/<username>")
def user_create(username):
    return insert_user(username)

@app.route("/chat/adduser/")
def chat_adduser():
    user_id = request.args.get("user")
    chat_id = request.args.get("chat")   
    if (user_id==None) or (chat_id==None):
        return {"error": {"id":654456,"mensage":"Insert user AND chat"}}
    else:
        return insert_usrinchat(user_id,chat_id)

@app.route("/chat/addmessage/")
def add_mensage():
    user_id = request.args.get("user")
    chat_id = request.args.get("chat")   
    text = request.args.get("text")
    if (user_id==None) or (chat_id==None):
        return {"error": {"id":654456,"mensage":"Insert user AND chat"}}
    elif text==None:
        return {"error": {"id":9999,"mensage":"No text inserted"}}
    else:   
        return insert_txt(text,user_id,chat_id)

@app.route("/chat/list/<chat_id>")
def mess_from_chat(chat_id):
    return get_msg(user_id=0,chat_id=chat_id,n=0,desc=True)

@app.route("/chat/sentiment/<chat_id>")
def sent_from_chat(chat_id):
    return obtain_sentiment(user_id=0,chat_id=chat_id,n_msg=0,last=True)

#app.run()
