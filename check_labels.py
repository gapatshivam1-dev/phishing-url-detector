import pandas as pd

df = pd.read_csv("data/phishing_data.csv")

# Show how many rows are 0 vs 1
print(df["target"].value_counts())

# Show average feature values for each class
print(df.groupby("target")[["isHttps", "nb_dots", "sensitive_words_count", "url_length"]].mean())