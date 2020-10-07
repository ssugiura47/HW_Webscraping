from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_info = mongo.db.marscol.find_one()
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scrape():
    mars = mongo.db.marscol   
    mars_info = scrape_mars.scrape()   
    mars.update({}, mars_info, upsert=True)
    print(mars_info)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
