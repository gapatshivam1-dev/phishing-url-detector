# features.py
import re
from urllib.parse import urlparse

def extract_features(url):
    original_url = url

    isHttps = 1 if original_url.lower().startswith("https://") else 0

    url_clean = re.sub(r'^https?://', '', original_url, flags=re.IGNORECASE)

    # Some real-world URLs are malformed and crash the parser (e.g. weird brackets).
    # If that happens, just treat path_length as 0 instead of crashing.
    try:
        parsed = urlparse("http://" + url_clean)
        path_length = len(parsed.path)
    except Exception:
        path_length = 0

    url_length = len(url_clean)
    at_symbol = 1 if "@" in url_clean else 0

    sensitive_words = ["login", "verify", "bank", "update", "secure", "account", "confirm", "signin"]
    sensitive_words_count = 1 if any(word in url_clean.lower() for word in sensitive_words) else 0

    nb_dots = url_clean.count(".")
    nb_hyphens = url_clean.count("-")
    nb_and = url_clean.count("&")
    nb_or = url_clean.count("|")
    nb_www = url_clean.lower().count("www")
    nb_com = url_clean.lower().count("com")
    nb_underscore = url_clean.count("_")

    return {
        "url_length": url_length,
        "at_symbol": at_symbol,
        "sensitive_words_count": sensitive_words_count,
        "path_length": path_length,
        "isHttps": isHttps,
        "nb_dots": nb_dots,
        "nb_hyphens": nb_hyphens,
        "nb_and": nb_and,
        "nb_or": nb_or,
        "nb_www": nb_www,
        "nb_com": nb_com,
        "nb_underscore": nb_underscore
    }


if __name__ == "__main__":
    test_url = "http://www.secure-login-update.com/account/verify?user=test&id=123"
    result = extract_features(test_url)
    for key, value in result.items():
        print(f"{key}: {value}")