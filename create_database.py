#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 10:26:39 2020

@author: ordovas
"""

from sentimet.sentiment_functions import *
from api.endpoints import *
from db.sqlConnection import *
import requests
import random
from bson import json_util


# Function to create the dataset
def create_data():
    # Load the different users
    file = "raw/users.txt"
    with open(file, "r") as f:
        lines = f.readlines()
    
    usrs=[]
    for line in lines:
            usrs.append(line.split("\n")[0].split(","))
            
            
    # Load the names of the different chat rooms        
    file = "raw/chats.txt"
    with open(file, "r") as f:
        lines = f.readlines()
    
    chats=[]
    for line in lines:
            chats.append(line.split("\n")[0])
            
    # Load all the different test mensages
    file = "raw/text.txt"
    with open(file, "r") as f:
        lines = f.readlines()
    
    txts=[]
    for line in lines:
            txts.append(line.split("\n")[0])
    
    # Randomly shuffle the users and chat
    np.random.shuffle(usrs)
    np.random.shuffle(chats)
    # Randomly choose the members of each chat room        
    chats_memb = [random.sample(list(range(1,len(usrs))), random.randint(5,15)) for _ in range(len(chats))]
    memb_q=[ str(el)[1:-1].replace(" ","") for el in  chats_memb ]   
    

    
    url_ini = "http://127.0.0.1:5000"
    # BUILD INSERT USERS API QUERIES
    query_create_usr=[]
    for i in range(len(usrs)):
        query_create_usr.append(url_ini+"/user/create/"+usrs[i][1]+"?name="+usrs[i][0]+"&password="+usrs[i][2])
        
    # BUILD CREATE CHAT API QUERIES
    query_create_chat=[]
    for i in range(len(chats)):
        query_create_chat.append(url_ini+"/chat/create/"+chats[i]+"?members="+memb_q[i])    
    
     # BUILD INSERT TEXT MESSAGES API QUERIES
    query_insert_msg=[]
    for i in range(len(chats)):
        for usr in chats_memb[i]:
            for _ in range(random.randint(10,30)):
                msg = random.sample(txts,1)[0]
                query_insert_msg.append(url_ini+"/chat/addmessage/?chat="+str(i+1)+"&user="+str(usr)+"&text="+msg)
    
    # Random order of input of all messages
    np.random.shuffle(query_insert_msg)   
    
    # API requests to insert the data in SQL
    execute_query(query_create_usr)
    execute_query(query_create_chat)
    execute_query(query_insert_msg)  
    return query_create_usr,query_create_chat,query_insert_msg

# Function to execute a list of API queries
def execute_query(list_q):
    for q in list_q:
        data=requests.get(q)
    
    
#query_create_usr,query_create_chat,query_insert_msg =  create_data()   
  
    
    
