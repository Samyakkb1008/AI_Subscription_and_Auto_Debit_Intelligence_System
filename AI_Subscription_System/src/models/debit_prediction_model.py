import pandas as pd


def load_data(path):
    return pd.read_csv(path)


def predict_debit(df):

    df["Date"] = pd.to_datetime(df["Date"])

    results = []

    # Use only useful data
    df = df[df["Frequency"].isin(["Monthly", "Weekly"])]

    for (customer, merchant), group in df.groupby(["CustomerID", "Merchant"]):

        group = group.sort_values("Date")

        last_date = group["Date"].max()
        avg_amount = group["Amount"].mean()

        freq = group["Frequency"].iloc[0]

        # Predict next date based on frequency
        if freq == "Monthly":
            next_date = last_date + pd.Timedelta(days=30)
        elif freq == "Weekly":
            next_date = last_date + pd.Timedelta(days=7)

        next_date = next_date.date()

        results.append({
            "CustomerID": customer,
            "Merchant": merchant,
            "Frequency": freq,
            "Next_Debit_Date": next_date,
            "Predicted_Amount": round(avg_amount, 2)
        })

    return pd.DataFrame(results)


if __name__ == "__main__":

    input_path = "data/processed/final_transactions.csv"
    output_path = "outputs/predictions.csv"

    df = load_data(input_path)

    predictions = predict_debit(df)

    predictions.to_csv(output_path, index=False)

    print("✅ Prediction done")
    print(predictions.head())