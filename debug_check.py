import pandas as pd
from features import extract_features

# The URL that got wrongly classified
test_url = "http://secure-login-verify-account.com/@bank/update?user=confirm"
our_features = extract_features(test_url)

print("Our extracted features for this URL:")
for k, v in our_features.items():
    print(f"  {k}: {v}")

# Compare against dataset averages for each class
df = pd.read_csv("data/phishing_data.csv")
print("\nDataset averages per class (0 = phishing, 1 = safe):")
print(df.groupby("target").mean(numeric_only=True))