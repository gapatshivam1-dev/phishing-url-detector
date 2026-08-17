# train_model.py
# This script loads our dataset, trains a model to detect phishing URLs,
# tests how accurate it is, and saves the trained model to a file.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load the dataset
df = pd.read_csv("data/phishing_data.csv")
print("Dataset loaded. Shape:", df.shape)
print(df.head())

# 2. Separate features (X) from the label (y)
X = df.drop(["target", "valid_url"], axis=1)
y = df["target"]

# 3. Split into training data (80%) and testing data (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Create and train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Test the model on data it has never seen
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model accuracy:", round(accuracy * 100, 2), "%")
print("Detailed report:")
print(classification_report(y_test, predictions))

# 6. Save the trained model to a file so our website can use it later
joblib.dump(model, "model/model.pkl")
print("Model saved to model/model.pkl")