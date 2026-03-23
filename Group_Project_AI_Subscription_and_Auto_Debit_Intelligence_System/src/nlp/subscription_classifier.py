import pandas as pd
import json
 
# Load data
def load_data(path):
    return pd.read_csv(path)
 
 
# Load keywords
def load_keywords(path):
    with open(path, "r") as f:
        return json.load(f)
 
 
# Classify function
def classify(description, keywords):
    description = str(description).lower()
 
    for word in keywords["subscription_keywords"]:
        if word in description:
            return "Subscription"
    
    return "Non-Subscription"
 
 
# Apply classification
def detect_subscriptions(df, keywords):
    df["Transaction_Type"] = df["Description"].apply(
        lambda x: classify(x, keywords)
    )
    return df
 
 
# Main
if __name__ == "__main__":
 
    input_path = "data/processed/cleaned_transactions.csv"
    output_path = "data/processed/with_subscription_flag.csv"
    keyword_path = "src/nlp/keyword_dictionary.json"
 
    df = load_data(input_path)
    keywords = load_keywords(keyword_path)
 
    df = detect_subscriptions(df, keywords)
 
    df.to_csv(output_path, index=False)
 
    print("✅ Subscription detection done")