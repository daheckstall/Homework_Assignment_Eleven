from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

app = Flask(__name__)

#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
conn = "mongodb://localhost:27017/mars_data"
#mongo = pymongo(app)

client = pymongo.MongoClient(conn)
db = client.mongo_mars_data
collection = db.mars_data

@app.route("/")
def home():

    # Find data
    mars = client.db.collection.find()

    # return template and data
    return render_template("index.html", mars_data=mars)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    results = scrape_mars.scrape()

    # Store results into a dictionary
    mars_results = {
        "news_title": results["news_title"],
        "news_paragraph": results["news_paragraph"],
        "featured_image": results["featured_image"],
        "weather": results["weather"],
        "mars_stats": results["mars_df"],
        "hempisphere_images": results["images"]
        }  

    # Insert forecast into database
    client.db.collection.insert_one(mars_results)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)