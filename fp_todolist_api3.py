from flask import (
    Flask,
    request,
    jsonify,
)
import psycopg2
import urllib
import os

app = Flask(__name__)

# Set the environment variable for Google Cloud SQL connection
CLOUDSQL_CONNECTION_NAME = os.environ.get("CLOUDSQL_CONNECTION_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

@app.route("/api/tasks", methods=['GET'])
def get_items():
    connection_db = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=f"/cloudsql/{CLOUDSQL_CONNECTION_NAME}"
    )
    with connection_db:
        with connection_db.cursor() as cursor:
            cursor.execute("SELECT what_to_do, due_date, status FROM entries")
            entries = cursor.fetchall()
    tdlist = [
        dict(what_to_do=row[0], due_date=row[1], status=row[2]) for row in entries
    ]
    return jsonify(tdlist)

@app.route("/api/tasks", methods=["POST"])
def add_item():
    connection_db = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=f"/cloudsql/{CLOUDSQL_CONNECTION_NAME}"
    )
    with connection_db:
        with connection_db.cursor() as cursor:
            cursor.execute("INSERT INTO entries (what_to_do, due_date) VALUES (%s, %s)",
                           (request.json["what_to_do"], request.json["due_date"]))
            connection_db.commit()
    return jsonify({"result": True})

@app.route("/api/tasks/<item>", methods=["DELETE"])
def delete_item(item):
    item = urllib.parse.unquote(item)
    connection_db = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=f"/cloudsql/{CLOUDSQL_CONNECTION_NAME}"
    )
    with connection_db:
        with connection_db.cursor() as cursor:
            cursor.execute("DELETE FROM entries WHERE what_to_do=%s", (item,))
            connection_db.commit()
    return jsonify({"result": True})

@app.route("/api/tasks/<item>", methods=["PUT"])
def update_item(item):
    item = urllib.parse.unquote(item)
    connection_db = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=f"/cloudsql/{CLOUDSQL_CONNECTION_NAME}"
    )
    with connection_db:
        with connection_db.cursor() as cursor:
            cursor.execute("UPDATE entries SET status='done' WHERE what_to_do=%s", (item,))
            connection_db.commit()
    return jsonify({"result": True})

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001)