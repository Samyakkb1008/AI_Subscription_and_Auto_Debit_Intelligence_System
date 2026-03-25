# src/models/train_subscription_model.py

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from src.nlp.preprocess_text import clean_text

# 1. Load cleaned dataset
df = pd.read_csv("data/cleaned_transactions.csv")

# 2. Prepare training data
X = df["Description"].apply(clean_text)
y = df["SubscriptionFlag"]   # Ground truth from dataset

# 3. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. ML Pipeline (TF-IDF + Logistic Regression)
clf_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

# 5. Train model
clf_pipeline.fit(X_train, y_train)

# 6. Evaluate accuracy
accuracy = clf_pipeline.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# 7. Save model as .pkl
pickle.dump(
    clf_pipeline,
    open("src/models/saved_models/subscription_model.pkl", "wb")
)

print("Model saved → subscription_model.pkl")