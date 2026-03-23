import pandas as pd


# Load dataset
def load_data(file_path):
    df = pd.read_csv(file_path)
    print("✅ Data loaded")
    return df
 
 
# Clean dataset
def clean_data(df):
 
    # 1. Remove duplicates
    df = df.drop_duplicates()
 
    # 2. Remove missing values
    df = df.dropna()
 
    # 3. Convert Date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
 
    # 4. Convert text to lowercase
    df["Description"] = df["Description"].str.lower().str.strip()
    df["Merchant"] = df["Merchant"].str.lower().str.strip()
 
    # 5. Convert numeric columns
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce")
    df = df.dropna(subset=["Amount", "Balance"])
 
    # 6. Sort by date
    df = df.sort_values(by="Date")
 
    print("✅ Data cleaned")
    return df
 
 
# Save cleaned data
def save_data(df, output_path):
    df.to_csv(output_path, index=False)
    print("✅ Cleaned data saved")
 
 
# Main execution
if __name__ == "__main__":
 
    input_path = "data/subscription_dataset.csv"
    output_path = "data/processed/cleaned_transactions.csv"
 
    df = load_data(input_path)
    df = clean_data(df)
    save_data(df, output_path)