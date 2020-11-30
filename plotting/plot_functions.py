#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 13:23:59 2020

@author: ordovas
"""
import numpy as np
import matplotlib.pyplot as plt
from sentimet.sentiment_functions import obtain_sentiment
from db.sqlConnection import id_user_info,id_chat_info

# obtain_sentiment(user_id=0,chat_id=0,n_msg=0,last=True)
def plotting(user_id=0,chat_id=0,n_msg=0,last=True):
    # Loading data
    data=obtain_sentiment(user_id,chat_id,n_msg,last)
    data["sentiment"]['sentiment_stats']["list"]
    pos=data["sentiment"]['sentiment_stats']["list"]["pos"]
    neu=data["sentiment"]['sentiment_stats']["list"]["neu"]
    neg=data["sentiment"]['sentiment_stats']["list"]["neg"]
    x=list(range(len(pos)))
    
    #Creating title 
    tt=""
    if n_msg ==0:
        tt+="All mensages"
    elif last:
        tt+=f"Last {n_msg} mensages"
    else:
        tt+=f"First {n_msg} mensages"
     
    if user_id==0:
        tt+= " form all users"
    else:
        tt+= " from user='"+id_user_info(user_id)["name"]+"'"
 
    if chat_id==0:
        tt+= " in all chats"
    else:
        tt+= " in chat='"+id_chat_info(chat_id)["name"]+"'"   
        
    # Save figure if there is data
    if not(pos==[]):
        fig = plt.figure(figsize=(10,16))
        plt.subplot(3, 1, 1)
        plt.scatter(x,pos,color="green")
        plt.ylabel("Positive Score")
        plt.title(tt)
        plt.subplot(3, 1, 2)
        plt.scatter(x,neu,color="orange")
        plt.ylabel("Neutral Score")
        plt.subplot(3, 1, 3)
        plt.scatter(x,neg,color="red")
        plt.xlabel(f" USER ID = {user_id}   CHAT ID = {chat_id}")
        plt.ylabel("Negative Score")
        plt.savefig("plotting/result_query.png")
    
    # Return if the plot was dones
    return not(pos==[])


