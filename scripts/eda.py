import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn


def check_null_or_nan_or_empty(df):
    """
    Checks all columns in a DataFrame for null/NaN or empty string values.
    Prints columns with issues and returns a dictionary summarizing the results.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        dict: A dictionary with column names as keys and a boolean indicating
              whether the column contains null/NaN or empty string values.
    """
    if df.empty:
        print("The DataFrame is empty.")
        return {}

    results = {}
    for column in df.columns:
        has_null_or_nan = df[column].isnull().any()
        has_empty_strings = (df[column] == "").any() if df[column].dtype == "object" else False
        results[column] = has_null_or_nan or has_empty_strings

        if results[column]:
            print(f"Column '{column}' contains null/NaN or empty string values.")

    if any(results.values()):
        print("\nSummary:")
        for col, has_issues in results.items():
            if has_issues:
                print(f"  - {col}: Issues found")
    else:
        print("No null/NaN or empty string values found in the DataFrame.")

    return results



