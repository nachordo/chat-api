from sqlalchemy import create_engine
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




def insert_table(name):
    """
    INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
    VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway');
    INSERT INTO Customers (CustomerName, City, Country)
    VALUES ('Cardinal', 'Stavanger', 'Norway');
    """
    query = f"INSERT INTO chat.chats (name) VALUES ('{name}');"
    res = conn.execute(query)
    return serialize(res)

def get_table(name):
    query = f"SELECT * FROM lab_advanced.{name};"
    res = conn.execute(query)
    return serialize(res)
