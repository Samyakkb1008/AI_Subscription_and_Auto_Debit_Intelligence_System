import pandas as pd
from src.utils.config import RAW_DATA_PATH, CLEANED_DATA_PATH
from src.utils.helpers import load_csv, save_csv

def clean_data(df):

    # 1. Remove duplicates
    df = df.drop_duplicates()

    # 2. Fix Date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    # 3. Fix numeric columns
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce")

    df = df.dropna(subset=["Amount", "Balance"])

    # 4. Sort data properly
    df = df.sort_values(by=["CustomerID", "Date", "TransactionID"])

    # 5. Add Month column
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    # 6. Add Day of Week
    df["DayOfWeek"] = df["Date"].dt.day_name()

    # 7. Add Debit / Credit Type
    df["TransactionType"] = df["Amount"].apply(lambda x: "Credit" if x > 0 else "Debit")

    print("✅ Data cleaned successfully")
    return df


if __name__ == "__main__":

    df = load_csv(RAW_DATA_PATH)
    df = clean_data(df)
    save_csv(df, CLEANED_DATA_PATH)