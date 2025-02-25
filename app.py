from flask import Flask, request, render_template
import numpy as np
import pickle
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from feature import FeatureExtraction
from convert import conversion
import warnings
import logging
import urllib.parse  # To encode password safely

# Suppress warnings
warnings.filterwarnings('ignore')

# Initialize Flask app
app = Flask(__name__)

# Enable Debug Mode
app.debug = True
app.logger.setLevel(logging.DEBUG)

# MongoDB Connection (Replace `your_password_here` with actual password)
password = urllib.parse.quote("your_password_here")  # URL encode special characters
MONGO_URI = f"mongodb+srv://karanramesh0124:{password}@cluster0.qrdid.mongodb.net/phishing_db?retryWrites=true&w=majority"

# MongoDB Connection Setup
try:
    app.logger.info("🔵 Attempting to connect to MongoDB...")
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    client.admin.command('ping')  # Test connection
    db = client["phishing_db"]  # Database Name
    collection = db["predictions"]  # Collection Name

    # Ensure collection exists
    if "predictions" not in db.list_collection_names():
        db.create_collection("predictions")

    app.logger.info("✅ Successfully connected to MongoDB!")
except pymongo.errors.ConnectionFailure as e:
    app.logger.error(f"❌ MongoDB Connection Failed: {e}")
    client = None
    db = None
    collection = None
except pymongo.errors.ConfigurationError as e:
    app.logger.error(f"❌ MongoDB Configuration Error: {e}")
    client = None
    db = None
    collection = None
except Exception as e:
    app.logger.error(f"❌ Unexpected MongoDB Error: {e}")
    client = None
    db = None
    collection = None

# Load Pre-trained Model
try:
    with open("newmodel.pkl", "rb") as file:
        gbc = pickle.load(file)
    app.logger.info("✅ Model loaded successfully.")
except Exception as e:
    app.logger.error(f"❌ Error loading model: {e}")
    gbc = None  # Handle cases where model fails to load

# Home Page Route
@app.route("/", methods=["GET"])
def home():
    app.logger.debug("🔵 Rendering home page")

    # Fetch last 10 predictions if MongoDB is connected
    past_predictions = list(collection.find().sort("_id", -1).limit(10)) if collection else []

    return render_template("index.html", name=None, error=None, past_predictions=past_predictions)

# Prediction Route
@app.route('/result', methods=['POST'])
def predict():
    try:
        url = request.form.get("url")
        if not url:
            app.logger.warning("⚠️ No URL provided.")
            return render_template("index.html", error="Please enter a valid URL.", name=None)

        app.logger.debug(f"🔍 URL received for prediction: {url}")

        # Feature Extraction
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, -1)
        app.logger.debug(f"📊 Features extracted: {x}")

        # Make Prediction
        if gbc is not None:
            y_pred = gbc.predict(x)[0]
            app.logger.debug(f"🧠 Prediction result: {y_pred}")

            name = conversion(url, int(y_pred))

            # Store in MongoDB
            if collection:
                collection.insert_one({"url": url, "prediction": name})

            return render_template("index.html", name=name, error=None)
        else:
            app.logger.error("❌ Model not loaded. Cannot make predictions.")
            return render_template("index.html", error="Model not available.", name=None)

    except Exception as e:
        app.logger.error(f"❌ Error during prediction: {e}")
        return render_template("index.html", error="An error occurred during prediction.", name=None)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
