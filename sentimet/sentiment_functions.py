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

nltk.download('stopwords')
nltk.download("vader_lexicon")
#stopwords.words('english')
sia = SentimentIntensityAnalyzer()

def unwrapped_msg(user_id=0,chat_id=0,n_msg=0,last=True):
    queried_msg = get_msg(user_id,chat_id,n_msg,last) #res["msg_query"][0]["id_msg"]
    res = [el["txt"] for el in queried_msg["msg_query"]]
    return res

def obtain_sentiment(user_id=0,chat_id=0,n_msg=0,last=True):
    msgs = get_msg(user_id,chat_id,n_msg,last)
    dic = {"list":msgs, "stats":compute_sentiment(msgs)}
    res={"user_id":user_id, "chat_id":chat_id, "number_msg":n_msg, "from_last":last, "sentiment":dic}
    return res
    
    
def sentiment_stats(lst):
    pos_list = [el["pos"] for el in lst]
    neg_list = [el["neg"] for el in lst]
    neu_list = [el["neu"] for el in lst]
    dic={"mean": {"neg":np.mean(neg_list) , "neu":np.mean(neu_list) , "pos":np.mean(pos_list)} }
    dic["stdv"] = {"neg":np.std(neg_list) , "neu":np.std(neu_list) , "pos":np.std(pos_list)}
    dic["median"] = {"neg":np.median(neg_list) , "neu":np.median(neu_list) , "pos":np.median(pos_list)}
    return {"not":"today"}
     
    
    
def compute_sentiment(mensages):
    return [ sia.polarity_scores(msg) for msg in mensages ]
    