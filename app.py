from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():

# Retrieve the Mongo DB information 
    listings = mongo.db.collection.find_one()
    return render_template("index.html", collections=listings)


@app.route("/scrape")
def scraper():

# Run the scrape function
    listings_data = scrape_mars.scrape()

# Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, listings_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
