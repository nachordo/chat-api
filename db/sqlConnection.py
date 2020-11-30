from sqlalchemy import create_engine,insert
from dotenv import load_dotenv
import pymysql
import os

from json import dumps
from sqlalchemy.orm import class_mapper

# Obtains the user and password from environment variables
load_dotenv()
user = os.getenv("SQLUSER")
password = os.getenv("SQLPASS")

# Initiantes the MySQL connection
mysql_url = f'mysql+pymysql://{user}:{password}@localhost'
engine = create_engine(mysql_url)
conn = engine.connect()


# Function to create a chat room
def insert_chat(name,lst):
    query = f"SELECT * FROM chat.chats WHERE name='{name}';"
    res = list(conn.execute(query))
    if res == []:
        query = f"INSERT INTO chat.chats (name) VALUES ('{name}');"
        res = conn.execute(query)
        res = get_chat_info(name)
        for el in lst:
            insert_usrinchat(el,res["id_chat"])
        return res
    else:
        return {"error": {"id":1020220201,"mensage":"Chat already exists"}}

# Function to insert users in chat room
def insert_usrinchat(user_id,chat_id):
    query = f"SELECT * FROM chat.participants WHERE (chats_id_chat={chat_id} AND users_id_usr={user_id});"
    res = list(conn.execute(query))
    if res == []:
        query = f"INSERT INTO chat.participants  VALUES ({user_id},{chat_id});"
        res = conn.execute(query)
        
        return {"chat_id":chat_id}
    else:
        return {"error": {"id":4224,"mensage":f"USRID={user_id} already in CHATID={chat_id}. Ignoring your commands."}}

# Function to obtain the chat info    
def get_chat_info(name):
    query = f"SELECT * FROM chat.chats WHERE name='{name}';"
    res = list(conn.execute(query))[0]
    columns = ["id_chat","name"]
    dic = {columns[i]:res[i] for i in range(len(columns))}
    return dic

# Function to obtain user info
def user_info(username):
    query = f"SELECT id_usr,name,username FROM chat.users WHERE username='{username}';"
    res = list(conn.execute(query))[0]
    columns = ["id_usr","name","username"]
    dic = {columns[i]:res[i] for i in range(len(columns))}
    return dic  

# Function to obtain the chat info    
def id_chat_info(id_chat):
    query = f"SELECT * FROM chat.chats WHERE id_chat='{id_chat}';"
    res = list(conn.execute(query))[0]
    columns = ["id_chat","name"]
    dic = {columns[i]:res[i] for i in range(len(columns))}
    return dic

# Function to obtain user info
def id_user_info(id_user):
    query = f"SELECT id_usr,name,username FROM chat.users WHERE id_usr='{id_user}';"
    res = list(conn.execute(query))[0]
    columns = ["id_usr","name","username"]
    dic = {columns[i]:res[i] for i in range(len(columns))}
    return dic  

# Function to create a new user
def insert_user(name,username,password):
    query = f"SELECT username FROM chat.users WHERE username='{username}';"
    res = list(conn.execute(query))
    if res == []:
        #query = f"INSERT INTO chat.users (username) VALUES ('{username}');"
        query = f'INSERT INTO chat.users (name,username,password) VALUES ("{name}","{username}","{password}");'
        res = conn.execute(query)     
        return user_info(username)
    else:
        return {"error": {"id":80022008,"mensage":"User already exists"}}  

# Function to insert a new message in the database
def insert_txt(text,user_id,chat_id):
    if not(is_usrinchat(user_id,chat_id)):
        return {"error":{"id":8030220308,"mensage":"Input wrong and very wrong"}}   
    
    query = f'INSERT INTO chat.messages (txt,users_id_usr,chats_id_chat)  VALUES ("{text}",{user_id},{chat_id});'
    res = conn.execute(query)
    res = get_msg(user_id=user_id,chat_id=chat_id,n=1,desc=True)
    return {"id_msg":res["msg_query"][0]["id_msg"]}
  
# Function to check if an user is in the database
def is_usrinchat(user_id,chat_id):
    query = f'SELECT * FROM chat.participants WHERE (chats_id_chat={chat_id} AND users_id_usr={user_id});'
    res = list(conn.execute(query))
    return not(res == [])

# Fonction to obtain all the messages with certain conditions
def get_msg(user_id=0,chat_id=0,n=1,desc=True):  
    #order
    if desc:
        dc="ORDER BY id_msg DESC"
    else:
        dc="ORDER BY id_msg ASC"
    
    #number
    if n>0:
        nc=f" LIMIT {n}"
    else:
        nc=""
    
    if (user_id !=0) and (chat_id == 0):
        query=f"SELECT * FROM chat.messages WHERE users_id_usr={user_id} {dc}{nc};"
    elif (user_id ==0) and (chat_id != 0):
        query=f"SELECT * FROM chat.messages WHERE chats_id_chat={chat_id} {dc}{nc};"
    elif (user_id !=0) and (chat_id != 0):
        query=f"SELECT * FROM chat.messages WHERE (chats_id_chat={chat_id} AND users_id_usr={user_id}) {dc}{nc};"
    else:
        query=f"SELECT * FROM chat.messages {dc} {nc};"
        
    query_res = list(conn.execute(query))
    columns = ["id_msg","text","user_id","chat_id"]
    res=[]
    for el in query_res:
        res.append( {columns[i]:el[i] for i in range(len(columns))} )
    return {"msg_query":res}  

