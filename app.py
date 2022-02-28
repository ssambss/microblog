from flask import Flask, render_template, request
from jinja2 import Template
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
import os


load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.mblog


    @app.route("/", methods=["GET", "POST"])
    def home():
        #Gets the content from the "content" textarea and inserts the entry and the date to db
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%d-%m-%Y")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        #Retrieves entries from the db with and shortens the date
        entries_with_date = [
            (
                entry["content"], 
                entry["date"], 
                datetime.datetime.strptime(entry["date"], "%d-%m-%Y").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries_with_date=entries_with_date)

    return app

