import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# --------------------------
# CONFIGURATION
# --------------------------
NUM_CUSTOMERS = 500
DAYS = 180
MIN_BALANCE = 200        # below this = low balance state
START_DATE = datetime(2025, 1, 1)

SUBSCRIPTION_SERVICES = [
    ("Netflix", 499),
    ("Spotify", 199),
    ("Amazon Prime", 999),
    ("Electricity Bill", 1500),
    ("Gym Membership", 1200)
]

RANDOM_MERCHANTS = [
    "Zomato", "Swiggy", "Uber", "Flipkart", "Reliance Smart",
    "DMart", "Petrol Pump", "Medical Store", "Cafe Coffee Day"
]

# ---------------------------------------------
# MAIN GENERATOR FUNCTION
# ---------------------------------------------
def generate_dataset():

    rows = []
    transaction_id = 1

    for cust in range(1, NUM_CUSTOMERS + 1):

        customer_id = f"C{cust}"

        # Initial balance
        balance = random.randint(5000, 20000)

        # Choose user subscriptions (1–3 per user)
        user_subs = random.sample(SUBSCRIPTION_SERVICES, random.randint(1, 3))

        # Fixed subscription billing days
        sub_days = {m: random.randint(1, 28) for (m, _) in user_subs}

        # Fixed salary day
        salary_day = random.randint(1, 5)

        current_date = START_DATE

        # For each day in 6 months
        for _ in range(DAYS):

            # --------------------------
            # 1. SALARY CREDIT
            # --------------------------
            if current_date.day == salary_day:
                salary_amount = random.randint(20000, 50000)
                balance += salary_amount

                rows.append([
                    customer_id,
                    f"T{transaction_id}",
                    current_date,
                    "Salary Credit",
                    "Employer",
                    salary_amount,
                    balance,
                    0          # SubscriptionFlag
                ])
                transaction_id += 1

            # --------------------------
            # 2. SUBSCRIPTION PAYMENTS
            # --------------------------
            for (merchant, amt) in user_subs:

                if current_date.day == sub_days[merchant]:

                    # Check for sufficient balance
                    if balance >= amt:
                        balance -= amt

                    rows.append([
                        customer_id,
                        f"T{transaction_id}",
                        current_date,
                        f"{merchant} Subscription",
                        merchant,
                        -amt,
                        balance,
                        1       # SubscriptionFlag
                    ])
                    transaction_id += 1

            # --------------------------
            # 3. RANDOM EXPENSES
            # --------------------------
            for _ in range(random.randint(0, 2)):

                merchant = random.choice(RANDOM_MERCHANTS)
                amt = random.randint(100, 2000)

                # Only debit if allowed (balance must not fall below MIN_BALANCE)
                if balance - amt >= MIN_BALANCE:
                    balance -= amt

                rows.append([
                    customer_id,
                    f"T{transaction_id}",
                    current_date,
                    f"Payment to {merchant}",
                    merchant,
                    -amt,
                    balance,
                    0        # SubscriptionFlag
                ])
                transaction_id += 1

            # Next day
            current_date += timedelta(days=1)

    # Convert to DF
    df = pd.DataFrame(rows, columns=[
        "CustomerID",
        "TransactionID",
        "Date",
        "Description",
        "Merchant",
        "Amount",
        "Balance",
        "SubscriptionFlag"
    ])

    return df

# ---------------------------------------------
# EXECUTION
# ---------------------------------------------
if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("..\\data\\Synthetic\\subscription_dataset.csv", index=False)
    print("subscription_dataset.csv generated successfully!")
    print("Total transactions:", len(df))