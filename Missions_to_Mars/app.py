from flask import Flask, render_template, redirect
import scrape 
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/craiglist_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    #listings = mongo.db.listings.find_one()
    mars_info = []

    return render_template("index.html", mars_info = mars_info)

@app.route("/scrape")
def scraper():
    mars_info = scrape.scrape()

    #listings = mongo.db.listings
    #listings.update({}, listings_result, upsert = True)

    return redirect("/", code = 302)


if __name__ == "__main__":
    app.run(debug = True)