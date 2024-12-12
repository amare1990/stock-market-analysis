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
            print(f"Column '{column}' contains {df[column].value_counts} null/NaN or empty string values.")

    if any(results.values()):
        print("\nSummary:")
        for col, has_issues in results.items():
            if has_issues:
                print(f"  - {col}: Issues found")
    else:
        print("No null/NaN or empty string values found in the DataFrame.")

    return results


def analyze_data(df):
    """
    Analyzes textual data and publication trends from the dataset.

    Args:
        df (pd.DataFrame): The dataset containing the columns ['headline', 'url', 'publisher', 'date', 'stock'].

    Returns:
        dict: A dictionary with results for each analysis.
    """

    # 1. Basic statistics for textual lengths (headline length)
    df['headline_length'] = df['headline'].apply(len)
    headline_stats = df['headline_length'].describe(include='object')  # Basic statistics (count, mean, std, min, max, etc.)

    # 2. Count the number of articles per publisher
    publisher_counts = df['publisher'].value_counts()  # Count articles per publisher

    # 3. Analyze publication dates to see trends over time
    # Convert the date column to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # Count articles by date
    daily_article_count = df.groupby(df['date'].dt.date).size().sort_values(ascending=False)  # Articles per day

    # Prepare results to return
    results = {
        'Headline_stats': headline_stats,
        'Publisher_counts': publisher_counts,
        'Daily_article_count': daily_article_count
    }

    return results


