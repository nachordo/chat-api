from api.app import app
from flask import request, send_from_directory
from db.mongoConnection import get_company, insert_data
from db.sqlConnection import get_table
from bson import json_util
import os
from random import choice

# Decorators
@app.route("/")
def hello_world():
    return {"hello": "World!"}

@app.route("/help")
def help():
    return {"welcome":"Welcome to my API"}


@app.route("/sql/<name>")
def sql(name):
    return json_util.dumps(list(get_table(name)))

app.run()
