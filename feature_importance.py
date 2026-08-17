import joblib
import pandas as pd

model = joblib.load("model/model.pkl")

# Show which features the model relies on most
importances = pd.Series(model.feature_importances_, index=model.feature_names_in_)
importances = importances.sort_values(ascending=False)
print("Feature importance (most influential first):")
print(importances)

# Compare against dataset averages per class again
df = pd.read_csv("data/phishing_data.csv")
print("\nDataset averages per class (0 = phishing, 1 = safe):")
print(df.groupby("target").mean(numeric_only=True))