# src/nlp/preprocess_text.py

"""
    Cleans transaction text for NLP processing.
    - lowercasing
    - punctuation removal
    - digit removal
    - extra space removal
"""
def clean_text(text):
    import re, string
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

