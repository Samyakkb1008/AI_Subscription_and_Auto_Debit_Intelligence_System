# Recurring Pattern Detection
"""
Recurring Pattern Detection Module
----------------------------------
This module implements BRD-FR4 requirements:

✔ Detect recurring transactions
✔ Detect frequency (MONTHLY, WEEKLY)
✔ Detect recurring dates
✔ Predict next expected transaction date
✔ Handles month-end edge cases using relativedelta

This script can be imported and used across:
- ML model building
- Risk scoring
- Streamlit UI
"""

import pandas as pd
import numpy as np
from datetime import timedelta
from dateutil.relativedelta import relativedelta


def compute_intervals(dates):
    """
    Compute day gaps between consecutive transaction dates.
    Used to classify recurrence type.
    """
    dates = sorted(dates)
    intervals = [
        (dates[i] - dates[i - 1]).days
        for i in range(1, len(dates))
    ]
    return intervals


def classify_recurrence(intervals):
    """
    Classifies recurrence patterns:
    WEEKLY  → avg interval 5–9 days
    MONTHLY → avg interval 28–32 days
    """
    if len(intervals) < 2:
        return None

    avg_gap = np.mean(intervals)

    if 5 <= avg_gap <= 9:
        return "WEEKLY"

    if 28 <= avg_gap <= 32:
        return "MONTHLY"

    return None


def detect_recurring_patterns(df):
    """
    Main recurring pattern detector.

    Inputs:
        df = cleaned transactions dataframe
             must contain columns:
             ['CustomerID', 'Merchant', 'Date']

    Returns:
        patterns_df = dataframe with:
        CustomerID, Merchant,
        Recurrence, RecurringDay,
        LastTransactionDate, NextExpectedDate,
        TotalOccurrences
    """

    patterns = []

    # Ensure Date is datetime
    df["Date"] = pd.to_datetime(df["Date"])

    for customer in df["CustomerID"].unique():
        df_cust = df[df["CustomerID"] == customer]

        for merchant in df_cust["Merchant"].unique():
            df_cm = df_cust[df_cust["Merchant"] == merchant]

            # Need at least 3 occurrences to consider recurring
            if len(df_cm) < 3:
                continue

            dates = sorted(df_cm["Date"].tolist())
            intervals = compute_intervals(dates)

            recurrence = classify_recurrence(intervals)
            if recurrence is None:
                continue

            # Recurring day of month (most frequent)
            recurring_day = int(df_cm["Date"].dt.day.mode()[0])

            last_date = dates[-1]

            # Predict next expected date
            if recurrence == "WEEKLY":
                next_expected = last_date + timedelta(days=7)

            elif recurrence == "MONTHLY":
                # Handles 30th → Feb 28/29, 31st → month end, leap year
                next_expected = last_date + relativedelta(months=1)

            patterns.append({
                "CustomerID": customer,
                "Merchant": merchant,
                "Recurrence": recurrence,
                "RecurringDay": recurring_day,
                "LastTransactionDate": last_date.date(),
                "NextExpectedDate": next_expected.date(),
                "TotalOccurrences": len(df_cm)
            })

    return pd.DataFrame(patterns)


def save_patterns(df, output_path):
    """
    Save recurring patterns to CSV.
    """
    df.to_csv(output_path, index=False)
    print(f"Recurring patterns saved → {output_path}")


# Run as a script
if __name__ == "__main__":
    # Load cleaned data
    df = pd.read_csv("..\\data\\subscription_dataset_cleaned.csv")

    patterns_df = detect_recurring_patterns(df)

    save_patterns(patterns_df, "data/recurring_patterns.csv")

    print("Recurring pattern detection completed successfully.")