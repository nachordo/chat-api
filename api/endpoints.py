from api.app import app
from flask import request, send_from_directory
from db.sqlConnection import *
from sentimet.sentiment_functions import *
from plotting.plot_functions import plotting
from bson import json_util
import os
from random import choice
import time

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
    if last==None:
        last=True
    elif (last!="first") and (last!="last"):
        return {"error": {"id":3223,"mensage":"You must select which=first or which=last"}}
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
    return obtain_sentiment(user_id=user_id,chat_id=chat_id,n_msg=int(n),last=last)


# Obtain the distance (similarity) of the conversations between two chats
@app.route("/chat/distance/")
def get_chat_dist():
    chat_id_a = request.args.get("chat_id_a")   
    chat_id_b = request.args.get("chat_id_b")   
    dist = request.args.get("dist")  
    if dist==None:
        dist="euclidean"
    elif (dist!="euclidean") and (dist!="cosine"):
        return {"error": {"id":7654567,"mensage":"Wrong distance"}}

    return chat_dist(chat_id_a,chat_id_b,dist)

# Obtain the distance (similarity) of the conversations between two users
@app.route("/user/distance/")
def get_user_dist():
    user_id_a = request.args.get("user_id_a")   
    user_id_b = request.args.get("user_id_b")   
    dist = request.args.get("dist")    
    if dist==None:
        dist="euclidean"
    elif (dist!="euclidean") and (dist!="cosine"):
        return {"error": {"id":7654567,"mensage":"Wrong distance"}}
    return users_dist(user_id_a,user_id_b,dist)

@app.route("/plot/")
def plotter():
    user_id = request.args.get("user_id")   
    chat_id = request.args.get("chat_id")   
    n = request.args.get("n_msg") 
    last   = request.args.get("which") 
    #Defensive programming "which"
    if last==None:
        last=True
    elif (last!="first") and (last!="last"):
        return {"error": {"id":3223,"mensage":"You must select which=first or which=last"}}
    else:
        last=="last"
    #Defensive programming
    if user_id==None:
        user_id=0
    if chat_id==None:
        chat_id=0
    if n==None:
        n=0     
    directory = os.getcwd()+"/plotting"
    result=plotting(user_id,chat_id,n,last)
    if result:
        return send_from_directory(directory=directory, filename="result_query.png", as_attachment=True)
    else:
        return {"error": {"id":436909634,"mensage":"The user is not in the chat"}}        

#app.run()
#(ironhack) [ordovas@localhost chat-api]$ export FLASK_APP=main.py
#(ironhack) [ordovas@localhost chat-api]$ export FLASK_DEBUG=true
#(ironhack) [ordovas@localhost chat-api]$ python3 -m flask run
#http://127.0.0.1:5000/plot/?which=last&chat_id=6&user_id=25
#http://127.0.0.1:5000/plot/?which=last&chat_id=8&user_id=24