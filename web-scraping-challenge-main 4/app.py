from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route("/")
def home():
    
    check = mongo.db.list_collection_names()

    if "collection" in check:
        mars_data = mongo.db.collection.find_one()
        return render_template("index.html", mars=mars_data)  
    else:
        place_holder = {"hemisphere_image_urls":["","","",""]}
        return render_template("index.html", mars=place_holder)
        
    # Return template and data

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database
    mongo.db.collection.insert_one(mars_data)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
