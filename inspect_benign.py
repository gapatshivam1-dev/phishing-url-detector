import pandas as pd
from features import extract_features

df = pd.read_csv("data/raw_urls.csv")
df = df[df["type"].isin(["phishing", "benign"])]

# Show 10 sample benign URLs exactly as they appear in the dataset
print("Sample BENIGN URLs from dataset:")
print(df[df["type"] == "benign"]["url"].head(10).to_string())

print("\nSample PHISHING URLs from dataset:")
print(df[df["type"] == "phishing"]["url"].head(10).to_string())

# Check average isHttps for each class using our feature extractor
df["label"] = df["type"].apply(lambda x: 1 if x == "phishing" else 0)
sample = df.sample(2000, random_state=1)
sample_features = sample["url"].apply(lambda u: extract_features(str(u)))
features_df = pd.DataFrame(list(sample_features))
features_df["label"] = sample["label"].values

print("\nAverage isHttps per class (0=benign, 1=phishing):")
print(features_df.groupby("label")["isHttps"].mean())
print("\nAverage url_length per class:")
print(features_df.groupby("label")["url_length"].mean())