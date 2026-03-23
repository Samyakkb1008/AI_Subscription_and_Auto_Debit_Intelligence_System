# Latest Balance vs Predicted Amount
import pandas as pd


def load_data(transactions_path, predictions_path):
    df = pd.read_csv(transactions_path)
    pred = pd.read_csv(predictions_path)
    return df, pred


def calculate_risk(df, pred):

    df["Date"] = pd.to_datetime(df["Date"])

    results = []

    for i, row in pred.iterrows():

        customer = row["CustomerID"]
        merchant = row["Merchant"]
        predicted_amount = row["Predicted_Amount"]

        # Get customer + merchant data
        customer_data = df[(df["CustomerID"] == customer) & (df["Merchant"] == merchant)]

        # Get latest balance
        latest_row = customer_data.sort_values("Date").iloc[-1]
        latest_balance = latest_row["Balance"]

        # Risk logic
        if latest_balance >= predicted_amount:
            risk = "Low"
        else:
            risk = "High"

        results.append({
            "CustomerID": customer,
            "Merchant": merchant,
            "Predicted_Amount": predicted_amount,
            "Balance": latest_balance,
            "Risk_Level": risk
        })

    return pd.DataFrame(results)


if __name__ == "__main__":

    transactions_path = "data/processed/final_transactions.csv"
    predictions_path = "outputs/predictions.csv"
    output_path = "outputs/risk_scoring_output.csv"

    df, pred = load_data(transactions_path, predictions_path)

    risk_df = calculate_risk(df, pred)

    risk_df.to_csv(output_path, index=False)

    print("✅ Risk scoring done")
    print(risk_df.head())