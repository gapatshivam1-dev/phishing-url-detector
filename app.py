from flask import Flask, render_template, request
import joblib
import pandas as pd
from features import extract_features
from urllib.parse import urlparse

app = Flask(__name__)
model = joblib.load("model/model.pkl")

# Well-known trusted domains — checked before the ML model runs.
# This mirrors how real-world browsers/security tools handle known-safe sites.
TRUSTED_DOMAINS = {
    "google.com", "youtube.com", "facebook.com", "amazon.com", "wikipedia.org",
    "microsoft.com", "apple.com", "github.com", "linkedin.com", "instagram.com",
    "twitter.com", "x.com", "netflix.com", "gmail.com", "yahoo.com"
}

def is_trusted_domain(url):
    try:
        domain = urlparse(url if "://" in url else "http://" + url).netloc.lower()
        domain = domain.replace("www.", "")
        return domain in TRUSTED_DOMAINS
    except Exception:
        return False

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    confidence = None
    submitted_url = None

    if request.method == "POST":
        submitted_url = request.form["url"]

        if is_trusted_domain(submitted_url):
            result = "Safe"
            confidence = 99.0
        else:
            features = extract_features(submitted_url)
            input_df = pd.DataFrame([features])
            input_df = input_df[model.feature_names_in_]

            prediction = model.predict(input_df)[0]
            probabilities = model.predict_proba(input_df)[0]

            if prediction == 1:
                result = "Phishing"
                confidence = round(probabilities[1] * 100, 2)
            else:
                result = "Safe"
                confidence = round(probabilities[0] * 100, 2)

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        submitted_url=submitted_url
    )

if __name__ == "__main__":
    app.run(debug=True)