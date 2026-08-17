from features import extract_features
import joblib
import pandas as pd

model = joblib.load("model/model.pkl")

test_url = "https://www.google.com"
features = extract_features(test_url)

print("Extracted features:")
for k, v in features.items():
    print(f"  {k}: {v}")

print("\nModel expects these columns in this order:")
print(list(model.feature_names_in_))

input_df = pd.DataFrame([features])
input_df = input_df[model.feature_names_in_]

prediction = model.predict(input_df)[0]
probabilities = model.predict_proba(input_df)[0]

print("\nPrediction:", prediction)
print("Probabilities:", probabilities)