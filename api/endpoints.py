from api.app import app
from flask import request, send_from_directory
from db.sqlConnection import *
from sentimet.sentiment_functions import *
from bson import json_util
import os
from random import choice

@app.route("/")
def hello_world():
    return {"welcome":"Welcome to the API of my project", "alumn":"Nacho"}


# Creates a chat room with a list of members
@app.route("/chat/create/<name>")
def chat_create(name):
    members = request.args.get("members")
    members=members.split(",")
    lst = list(map(int, members))
    return insert_chat(name,lst)

# Creates a new user
@app.route("/user/create/<username>")
def user_create(username):
    name = request.args.get("name")
    password = request.args.get("password")
    return insert_user(name,username,password)

# Adds an user to an extisting chat room
@app.route("/chat/adduser/")
def chat_adduser():
    user_id = request.args.get("user")
    chat_id = request.args.get("chat")   
    if (user_id==None) or (chat_id==None):
        return {"error": {"id":654456,"mensage":"Insert user AND chat"}}
    else:
        return insert_usrinchat(user_id,chat_id)

# Adds a texts message to a chat room posted by certain user
@app.route("/chat/addmessage/")
def add_mensage():
    user_id = request.args.get("user")
    chat_id = request.args.get("chat")   
    text = request.args.get("text")
    # To prevent errors I will change all " with ''
    text=text.replace('"', "''")
    if (user_id==None) or (chat_id==None):
        return {"error": {"id":654456,"mensage":"Insert user AND chat"}}
    elif text==None:
        return {"error": {"id":9999,"mensage":"No text inserted"}}
    else:   
        return insert_txt(text,user_id,chat_id)

# Lists all mensages from a chat room
@app.route("/chat/list/<chat_id>")
def mess_from_chat(chat_id):
    return get_msg(user_id=0,chat_id=chat_id,n=0,desc=False)

# Lists all mensages fom an user
@app.route("/user/list/<user_id>")
def mess_from_user(user_id):
    return get_msg(user_id=user_id,chat_id=0,n=0,desc=False)

# Obtain the sentiment of all mensages from a chat room
@app.route("/chat/sentiment/<chat_id>")
def sent_from_chat(chat_id):
    return obtain_sentiment(user_id=0,chat_id=chat_id,n_msg=0,last=True)

# Obtain the sentiment of all mensages from an user
@app.route("/user/sentiment/<user_id>")
def sent_from_user(user_id):
    return obtain_sentiment(user_id=user_id,chat_id=0,n_msg=0,last=True)

# Obtain the sentiment with cretain imputs
@app.route("/sentiment/")
def sentiment():
    user_id = request.args.get("user_id")   
    chat_id = request.args.get("chat_id")   
    n = request.args.get("n_msg") 
    last   = request.args.get("which") 
    #Defensive programming "which"
    if (last!="first") or (last!="last"):
        return {"error": {"id":3223,"mensage":"You must select which=first or which=last"}}
    elif last==None:
        last="last"
    else:
        last=="last"
    #Defensive programming
    if user_id==None:
        user_id=0
    if chat_id==None:
        chat_id=0
    if n==None:
        n=0     
    #Execute script
    return obtain_sentiment(user_id=user_id,chat_id=chat_id,n_msg=n,last=last)


# Obtain the distance (similarity) of the conversations between two chats
@app.route("/chat/distance/")
def get_chat_dist():
    chat_id_a = request.args.get("chat_id_a")   
    chat_id_b = request.args.get("chat_id_b")   
    dist = request.args.get("dist")    
    if (dist!="euclidean") or (dist!="cosine"):
        return {"error": {"id":7654567,"mensage":"Wrong distance"}}
    elif dist==None:
        dist="euclidean"
    return chat_dist(chat_id_a,chat_id_b,dist_type="euclidean")

# Obtain the distance (similarity) of the conversations between two users
@app.route("/user/distance/")
def get_user_dist():
    user_id_a = request.args.get("user_id_a")   
    user_id_b = request.args.get("user_id_b")   
    dist = request.args.get("dist")    
    if (dist!="euclidean") or (dist!="cosine"):
        return {"error": {"id":7654567,"mensage":"Wrong distance"}}
    elif dist==None:
        dist="euclidean"
    return user_dist(user_id_a,user_id_b,dist)



#app.run()
#(ironhack) [ordovas@localhost chat-api]$ export FLASK_APP=main.py
#(ironhack) [ordovas@localhost chat-api]$ export FLASK_DEBUG=true
#(ironhack) [ordovas@localhost chat-api]$ python3 -m flask run
#