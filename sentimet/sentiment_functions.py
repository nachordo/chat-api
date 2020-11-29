#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 20:40:20 2020

@author: ordovas
"""


import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from db.sqlConnection import get_msg
import numpy as np
import re

nltk.download('stopwords')
nltk.download("vader_lexicon")
#stopwords.words('english')
sia = SentimentIntensityAnalyzer()

# Obtain the sentiment of all the messages that meets some conditions
def obtain_sentiment(user_id=0,chat_id=0,n_msg=0,last=True):
    msgs = unwrapped_msg(user_id,chat_id,n_msg,last)
    dic = {"list":msgs, "sentiment":sentiment_stats(msgs)}
    res={"user_id":user_id, "chat_id":chat_id, "query_limit":n_msg, "from_last":last, "sentiment":dic}
    return res

# Returns lists with all the text messages and their IDs in other list
def unwrapped_msg(user_id=0,chat_id=0,n_msg=0,last=True):
    queried_msg = get_msg(user_id,chat_id,n_msg,last) #res["msg_query"][0]["id_msg"]
    txt = [el["text"] for el in queried_msg["msg_query"]]
    id_txt = [el["id_msg"] for el in queried_msg["msg_query"]]
    return {"mensages":txt, "id_mensages":id_txt}

# Computes the sentiment of each element of a list of strings
def compute_sentiment(mensages):
    return [sia.polarity_scores(msg) for msg in mensages["mensages"]]
    
# Computes sentiment statistics of a list of sentiment results
def sentiment_stats(msgs):
    lst=compute_sentiment(msgs)
    dic = {"msg_number":len(lst)}
    pos_list = [el["pos"] for el in lst]
    neg_list = [el["neg"] for el in lst]
    neu_list = [el["neu"] for el in lst]
    dic = {"list":{"neg":neg_list,"neu":neu_list,"pos":pos_list}}
    dic2={}
    dic2["mean"] = {"neg":np.mean(neg_list) , "neu":np.mean(neu_list) , "pos":np.mean(pos_list)} 
    dic2["stdv"] = {"neg":np.std(neg_list) , "neu":np.std(neu_list) , "pos":np.std(pos_list)}
    dic2["median"] = {"neg":np.median(neg_list) , "neu":np.median(neu_list) , "pos":np.median(pos_list)}
    dic["stats"] = dic2
    return dic

# Obtain the word count of all the messages that meets some conditions
def obtain_word_count(user_id=0,chat_id=0,n_msg=0,last=True):
    msgs = unwrapped_msg(user_id,chat_id,n_msg,last)
    dic = {"num_posts":msgs, "list":word_count(msgs["mensages"])}
    res={"user_id":user_id, "chat_id":chat_id, "query_limit":n_msg, "from_last":last, "word_count":dic}
    return res

# Computes the wor count of a list of strings
def word_count(lst):
    counts = dict()
    for string_raw in lst: 
        words = re.findall(r"[\w']*",string_raw)
        for word in words:
            if (word.lower() in stopwords.words('english')) or (word == ''):
                pass
            elif word.lower() in counts:
                counts[word.lower()] += 1
            else:
                counts[word.lower()] = 1  
    return counts
    