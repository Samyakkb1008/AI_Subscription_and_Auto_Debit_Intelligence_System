import pandas as pd
 
 
def load_data(path):
    return pd.read_csv(path)
 
 
def detect_patterns(df):
 
    df["Date"] = pd.to_datetime(df["Date"])
 
    result_rows = []
 
    for (customer, merchant), group in df.groupby(["CustomerID", "Merchant"]):
 
        group = group.sort_values("Date")
        group = group.drop_duplicates(subset=["Date"])
 
        # Only consider if at least 3 transactions exist
        if len(group) >= 3:
 
            # Calculate time gaps
            diffs = group["Date"].diff().dropna()
            avg_days = diffs.dt.days.mean()
 
            # Detect frequency
            if 25 <= avg_days <= 35:
                freq = "Monthly"
            elif 5 <= avg_days <= 10:
                freq = "Weekly"
            else:
                freq = "Irregular"
 
            # Predict next expected date
            next_date = group["Date"].max() + pd.Timedelta(days=avg_days)
 
            # Assign values to all rows of this group
            group["Frequency"] = freq
            group["Next_Expected_Date"] = next_date
 
        else:
            group["Frequency"] = "Not Recurring"
            group["Next_Expected_Date"] = None
 
        result_rows.append(group)
 
    final_df = pd.concat(result_rows)
 
    return final_df
 
 
if __name__ == "__main__":
 
    input_path = "data/processed/with_subscription_flag.csv"
    output_path = "data/processed/final_transactions.csv"
 
    df = load_data(input_path)
 
    df = detect_patterns(df)
 
    df.to_csv(output_path, index=False)
 
    print("✅ Pattern detection (Frequency + Next Date) done")

'''Code By Mansi'''
# import pandas as pd
# from datetime import timedelta
# def load_data(path):
#     return pd.read_csv(path)
 
# def detect_recurring_patterns(df):
#     """
#     Detects recurring payment patterns (monthly/weekly) for subscription transactions.
#     Adds two new columns: 'frequency' and 'next_expected_date'.
#     """
 
#     # Ensure Date column is in datetime format
#     df['Date'] = pd.to_datetime(df['Date'])
 
#     # Initialize new columns
#     df['frequency'] = None
#     df['next_expected_date'] = None
 
#     # Filter only subscription transactions
#     sub_df = df[df['Transaction_Type'] == "Subscription"]
 
#     # Group subscription transactions by Merchant
#     grouped = sub_df.groupby('Merchant')
 
#     for merchant, group in grouped:
#         # Sort the transactions by date
#         group = group.sort_values('Date')
 
#         # Calculate differences between consecutive dates
#         date_diffs = group['Date'].diff().dt.days.dropna()
 
#         if len(date_diffs) == 0:
#             # Only one transaction, cannot detect a pattern
#             continue
 
#         avg_gap = date_diffs.mean()
 
#         # Determine frequency based on average gap
#         if 25 <= avg_gap <= 35:
#             freq = "Monthly"
#             freq_days = 30
#         elif 5 <= avg_gap <= 9:
#             freq = "Weekly"
#             freq_days = 7
#         else:
#             freq = None
#             freq_days = None
 
#         # Assign frequency to rows in original df
#         df.loc[group.index, 'frequency'] = freq
 
#         # Compute next expected date for last recurring payment
#         if freq_days:
#             last_date = group['Date'].iloc[-1]
#             next_date = last_date + timedelta(days=freq_days)
#             df.loc[group.index[-1], 'next_expected_date'] = next_date
 
#     return df
 
 
# # -------------------------------
# # Example Usage (Person A Script)
# # -------------------------------
# if __name__ == "__main__":
#     # Load the dataset after NLP (Transaction_Type is already available)
#     # df = pd.read_csv("data\processed\with_subscription_flag.csv")
#     input_path = "data/processed/with_subscription_flag.csv"
 
#     df = load_data(input_path)
 
#     # Run pattern detection
#     enriched_df = detect_recurring_patterns(df)
 
#     # Save final enriched dataset for Person B
#     enriched_df.to_csv("data/final_dataset.csv", index=False)
 
#     print("Pattern detection complete. File saved as data/final_dataset.csv")