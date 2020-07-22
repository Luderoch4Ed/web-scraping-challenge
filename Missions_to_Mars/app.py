from flask import Flask, render_template 
import pymongo
import scrape_mars

#connect to MongoDB, mars_db
client = pymongo.MongoClient('mongodb://localhost:27017')
mongo = client.mars_db

app = Flask(__name__) # to get Flask working

@app.route("/") # for Flask
def index():
    mars = mongo.mars_info.find_one()
    return render_template("index.html",mars=mars)

@app.route("/scrape")
def scrape():
    mars_db = mongo.mars_info
    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Refresh data in Mongo db using update and upsert=True
    # mongo.db.collection.update({}, mars_data, upsert=True)
    mars_db.update({}, mars_data, upsert=True)
    return "Data update complete."
    
if __name__== "__main__":
    app.run(debug=True)

     