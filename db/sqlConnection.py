from sqlalchemy import create_engine,insert
from dotenv import load_dotenv
import pymysql
import os

from json import dumps
from sqlalchemy.orm import class_mapper

load_dotenv()

def serialize(model):
     """Transforms a model into a dictionary which can be dumped to JSON."""
     # first we get the names of all the columns on your model
     columns = [c.key for c in class_mapper(model.__class__).columns]
     # then we return their values in a dict
     return dict((c, getattr(model, c)) for c in columns)




user = os.getenv("SQLUSER")
password = os.getenv("SQLPASS")

mysql_url = f'mysql+pymysql://{user}:{password}@localhost'
engine = create_engine(mysql_url)
conn = engine.connect()



def insert_chat(name):
    query = f"SELECT * FROM chat.chats WHERE name='{name}';"
    res = list(conn.execute(query))
    if res == []:
        query = f"INSERT INTO chat.chats (name) VALUES ('{name}');"
        print(query)
        res = conn.execute(query)
        
        return get_chat_info(name)
    else:
        return {"error": {"id":1020220201,"mensage":"Chat already exists"}}




def user_info(username):
    query = f"SELECT id_usr,username FROM chat.users WHERE username='{username}';"
    res = list(conn.execute(query))[0]
    columns = ["id_usr","username"]
    dic = {columns[i]:res[i] for i in range(len(columns))}
    return dic  


def insert_user(username):
    query = f"SELECT username FROM chat.users WHERE username='{username}';"
    res = list(conn.execute(query))
    if res == []:
        query = f"INSERT INTO chat.users (username) VALUES ('{username}');"
        #query = f"INSERT INTO chat.users (username,password) VALUES ('{username},{password}');"
        res = conn.execute(query)
        
        return user_info(username)
    else:
        return {"error": {"id":80022008,"mensage":"Uer already exists"}}  

def get_table(name):
    query = f"SELECT * FROM lab_advanced.{name};"
    res = conn.execute(query)
    return list(res)

def get_chat_info(name):
    query = f"SELECT * FROM chat.chats WHERE name='{name}';"
    res = list(conn.execute(query))[0]
    columns = ["id_chat","name"]
    dic = {columns[i]:res[i] for i in range(len(columns))}
    return dic
"""
print(get_chat_info("PRU"))
print(insert_chat("PRU2"))
print(insert_chat("PRU2"))
"""