# build_and_train.py
# This script loads raw URLs, extracts features using our OWN features.py
# (so training and website always match), trains the model, and saves it.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from features import extract_features

# 1. Load raw data
df = pd.read_csv("data/raw_urls.csv")
print("Total rows loaded:", len(df))

# 2. Keep only phishing and benign rows (binary classification)
df = df[df["type"].isin(["phishing", "benign"])]
print("Rows after filtering to phishing/benign:", len(df))

# 3. Create our label: 1 = phishing, 0 = safe (benign)
df["label"] = df["type"].apply(lambda x: 1 if x == "phishing" else 0)

# 4. Extract features from EVERY url using our real features.py function
# This guarantees training features match website features exactly
print("Extracting features from URLs, this may take a minute...")
feature_rows = df["url"].apply(lambda u: extract_features(str(u)))
features_df = pd.DataFrame(list(feature_rows))

X = features_df
y = df["label"]

# 5. Split into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Train the model
model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluate
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print("\nModel accuracy:", round(accuracy * 100, 2), "%")
print(classification_report(y_test, predictions))

# 8. Save the model
joblib.dump(model, "model/model.pkl")
print("Model saved to model/model.pkl")