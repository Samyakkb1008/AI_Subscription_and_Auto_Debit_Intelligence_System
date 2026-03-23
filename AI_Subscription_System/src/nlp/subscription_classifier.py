# Trained the NLP model separately and integrated it into the pipeline using pickle for efficient reuse.
import pandas as pd
import pickle


# Load model + vectorizer
def load_models():
    model = pickle.load(open("src/models/saved_models/subscription_model.pkl", "rb"))
    vectorizer = pickle.load(open("src/models/saved_models/vectorizer.pkl", "rb"))
    return model, vectorizer


# Merchant extraction (same logic as notebook)
merchant_list = ["netflix", "spotify", "amazon", "electricity", "hotstar"]

def extract_merchant(text):
    text = str(text).lower()
    
    for merchant in merchant_list:
        if merchant in text:
            return merchant.capitalize()
    
    return "Unknown"


# Main function
def classify_transactions(df, model, vectorizer):

    # Extract merchant
    df["Merchant_Extracted"] = df["Description"].apply(extract_merchant)

    # Convert text to features
    X = vectorizer.transform(df["Description"])

    # Predict
    preds = model.predict(X)

    # Map labels
    df["Transaction_Type"] = preds
    df["Transaction_Type"] = df["Transaction_Type"].map({
        1: "Subscription",
        0: "Non-Subscription"
    })

    return df


if __name__ == "__main__":

    input_path = "data/cleaned_transactions.csv"
    output_path = "data/processed/with_subscription_flag.csv"

    df = pd.read_csv(input_path)

    model, vectorizer = load_models()

    df = classify_transactions(df, model, vectorizer)

    df.to_csv(output_path, index=False)

    print("✅ Subscription detection using ML done")
    print(df.head())

# import pandas as pd
# import json
 
# # Load data
# def load_data(path):
#     return pd.read_csv(path)
 
 
# # Load keywords
# def load_keywords(path):
#     with open(path, "r") as f:
#         return json.load(f)
 
 
# # Classify function
# def classify(description, keywords):
#     description = str(description).lower()
 
#     for word in keywords["subscription_keywords"]:
#         if word in description:
#             return "Subscription"
    
#     return "Non-Subscription"
 
 
# # Apply classification
# def detect_subscriptions(df, keywords):
#     df["Transaction_Type"] = df["Description"].apply(
#         lambda x: classify(x, keywords)
#     )
#     return df
 
 
# # Main
# if __name__ == "__main__":
 
#     input_path = "data/processed/cleaned_transactions.csv"
#     output_path = "data/processed/with_subscription_flag.csv"
#     keyword_path = "src/nlp/keyword_dictionary.json"
 
#     df = load_data(input_path)
#     keywords = load_keywords(keyword_path)
 
#     df = detect_subscriptions(df, keywords)
 
#     df.to_csv(output_path, index=False)
 
#     print("✅ Subscription detection done")