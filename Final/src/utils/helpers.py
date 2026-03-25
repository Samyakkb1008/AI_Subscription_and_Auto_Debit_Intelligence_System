# Helper functions
import pandas as pd
import numpy as np

def load_csv(path):
    return pd.read_csv(path)

def save_csv(df, path):
    df.to_csv(path, index=False)


# Without helpers.py?
# Your project becomes copy‑paste heavy and fragile.