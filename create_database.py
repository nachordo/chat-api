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


def create_data():
    file = "raw/users.txt"
    with open(file, "r") as f:
        lines = f.readlines()
    
    usrs=[]
    for line in lines:
            usrs.append(line.split("\n")[0].split(","))
            
            
            
    file = "raw/chats.txt"
    with open(file, "r") as f:
        lines = f.readlines()
    
    chats=[]
    for line in lines:
            chats.append(line.split("\n")[0])
            
            
    file = "raw/text.txt"
    with open(file, "r") as f:
        lines = f.readlines()
    
    txts=[]
    for line in lines:
            txts.append(line.split("\n")[0])
            
    chats_memb = [random.sample(list(range(1,len(usrs))), random.randint(5,15)) for _ in range(len(chats))]
    memb_q=[ str(el)[1:-1].replace(" ","") for el in  chats_memb ]   
    
    np.random.shuffle(usrs)
    np.random.shuffle(chats)
    
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
        
    np.random.shuffle(query_insert_msg)   
    
    execute_query(query_create_usr)
    execute_query(query_create_chat)
    execute_query(query_insert_msg)  
    return query_create_usr,query_create_chat,query_insert_msg
    
def execute_query(list_q):
    for q in list_q:
        data=requests.get(q)
    
    
#query_create_usr,query_create_chat,query_insert_msg =  create_data()   
  
    
    
