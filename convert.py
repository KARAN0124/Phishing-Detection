import re
import csv
import pickle
import requests
import os

# Load trained ML model (Replace 'newmodel.pkl' with actual model file)
def load_model(model_path="newmodel.pkl"):
    if os.path.exists(model_path):
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        return model
    else:
        print("Error: Model file not found!")
        return None

# Predict phishing status using ML model
def get_prediction(url, model):
    if model:
        # Assuming the model expects numerical features, extract them accordingly
        # Placeholder: Feature extraction logic needed
        # Example: features = extract_features(url)
        features = [0] * 10  # Dummy feature vector (replace with real extraction)
        prediction = model.predict([features])[0]
        return prediction  # 1 = Safe, 0 = Phishing
    return -1  # Default case if model fails

# Function to check if a URL is a shortened link
def shortlink(url):
    short_domains = (
        r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
        r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
        r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
        r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
        r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
        r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
        r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
        r'tr\.im|link\.zip\.net'
    )
    return -1 if re.search(short_domains, url, re.IGNORECASE) else 1  # -1 = Shortened URL, 1 = Normal URL

# Function to find URL in a CSV file
def find_url_in_csv(csv_file, target_url):
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row and len(row) > 0:  # Ensure row exists and is not empty
                    url = row[0].strip()
                    if url == target_url:
                        return url
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
    except IndexError:
        print("Error: CSV row structure is incorrect.")
    return None

# Function to handle URL conversion and classification
def conversion(url, prediction):
    if shortlink(url) == -1:
        return {"url": url, "status": "Not Safe", "message": "Shortened URL detected. Proceed with caution.", "prediction": -1}
    elif prediction == 1:
        return {"url": url, "status": "Safe", "message": "Proceed", "prediction": 1}
    else:
        return {"url": url, "status": "Not Safe", "message": "Potential phishing site detected.", "prediction": 0}

# Testing the script
if __name__ == "__main__":
    model = load_model()  # Load trained ML model
    url = "http://bit.ly/example"  # Example URL
    prediction = get_prediction(url, model)  # Replace with actual model-based prediction
    result = conversion(url, prediction)

    # Output result
    print(result)
