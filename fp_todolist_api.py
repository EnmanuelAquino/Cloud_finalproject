# RESTful API
from flask import (
    Flask,
    g,
    request,
    jsonify,
    Response,
)
import sqlite3
import urllib
import json
import psycopg2

#DATABASE = "todolist.db"
#create the connection of the elephant sql url inside the app.
POSTGREURL="postgres://rqdgmsop:TZ8znHp39kSnxR46QYkMDgf4HglPyxaA@otto.db.elephantsql.com/rqdgmsop"
connection_db=psycopg2.connect(POSTGREURL)

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URL']=POSTGREURL


@app.route("/api/tasks", methods=['GET']) # default method is GET
def get_items(): # this is the counterpart of show_list() from homework 3
    with connection_db:
        with connection_db.cursor() as cursor:
            cursor.execute("SELECT what_to_do, due_date, status FROM entries")
            entries=cursor.fetchall()
    tdlist = [
        dict(what_to_do=row[0], due_date=row[1], status=row[2]) for row in entries
    ]
    return jsonify(tdlist)


@app.route("/api/tasks", methods=["POST"])
def add_item():  # this is the counterpart of add_entry() from homework 3
    with connection_db:
        with connection_db.cursor() as cursor:
            cursor.execute("insert into entries (%s, %s);0,",
                             [request.json["what_to_do"], request.json["due_date"]])  
            entries=cursor.fetchall()
    return jsonify({"result": True})


@app.route("/api/tasks/<item>", methods=["DELETE"])
def delete_item(item):  # this is the counterpart of delete_entry() from homework 3
    item=urllib.parse.unquote(item)
    with connection_db:
        with connection_db.cursor() as cursor:
            cursor.execute("DELETE FROM entries WHERE what_to_do='"+item+"'")
    return jsonify({"result": True})


@app.route("/api/tasks/<item>", methods=["PUT"])
def update_item(item):  # this is the counterpart of mark_as_done() from homework 3
    item=urllib.parse.unquote(item)
    with connection_db:
        with connection_db.cursor() as cursor:
            cursor.execute("UPDATE entries SET status='done' WHERE what_to_do='"+item+"'")
    return jsonify({"result": True})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001)