# src/nlp/subscription_classifier.py
"""
    FULL NLP PIPELINE:
    1. Clean text
    2. Spell Correction (SymSpell)
    3. Lemmatization (NLTK)
    4. Keyword Detection
    5. spaCy ML Detection
    """

# src/nlp/subscription_classifier.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import spacy, json
from src.nlp.preprocess_text import clean_text

# Load model using absolute path
MODEL_PATH = os.path.abspath("src/models/saved_models/spacy_subscription_model")
nlp = spacy.load(MODEL_PATH)

with open("src/nlp/keyword_dictionary.json") as f:
    KEYWORDS = json.load(f)


# spell = SpellCorrector()

def detect_subscription(description, merchant):

    cleaned = clean_text(description)
    # corrected = spell.correct(cleaned)
    
    for key, cat in KEYWORDS.items():
            if key in cleaned:
                return {
                    "TransactionType": "Subscription",
                    "Merchant": merchant,
                    "Category": cat,
                    "DetectedBy": "Keyword",
                    "Score": 1.0
                }

    # spaCy detection
    doc = nlp(cleaned)
    score = float(doc.cats["SUBSCRIPTION"])

    if score >= 0.5:
        return {
            "TransactionType": "Subscription",
            "Merchant": merchant,
            "Category": "ml_detected",
            "DetectedBy": "spaCy",
            "Score": score
        }

    return {
        "TransactionType": "Non-Subscription",
        "Merchant": merchant,
        "Category": None,
        "DetectedBy": "spaCy",
        "Score": score
    }
