import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__, static_folder='templates')

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route('/scrape')
def scrapey():
    db = mongo.db.mars
    data = scrape()
    db.replace_one({}, data, upsert=True)

    return redirect("http://localhost:5000/", code=302)

@app.route('/')
def index():
    mars_info = mongo.db.mars.find_one()
    return render_template('index.html', info=mars_info)

if __name__ == "__main__":
    app.run(debug=True)