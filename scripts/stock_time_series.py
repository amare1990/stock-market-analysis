import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os

def analyze_publication_frequency(df, date_column):
    """
    Analyzes the publication frequency over time.

    Args:
        df (pd.DataFrame): Input DataFrame.
        date_column (str): Column containing datetime information.

    Returns:
        pd.DataFrame: Time-series data of publication frequencies.
    """
    # Convert the date column to datetime
    df[date_column] = pd.to_datetime(df[date_column])

    # Group by date and count publications
    daily_count = df.groupby(df[date_column].dt.date).size().reset_index(name='publication_count')

    # Plot publication frequency over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=daily_count, x=date_column, y='publication_count', marker='o')
    plt.title('Publication Frequency Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Publications')
    plt.grid(True)
    plt.show()

    # Ensure the 'plots' directory exists
    save_path = "/home/am/Documents/Software Development/10_Academy Training/week1/stock-market-analysis/plots/publication_frequency.png"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Save the plot to the specified path
    plt.savefig(save_path)

    # Optionally, show the plot
    plt.show()

    return daily_count
