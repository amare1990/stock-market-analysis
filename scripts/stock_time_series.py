import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

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

    return daily_count

def analyze_publishing_times(df, date_column):
    """
    Analyzes publishing times to find patterns during the day.

    Args:
        df (pd.DataFrame): Input DataFrame.
        date_column (str): Column containing datetime information.

    Returns:
        pd.DataFrame: Hourly publication frequencies.
    """
    # Convert the date column to datetime
    df[date_column] = pd.to_datetime(df[date_column])

    # Extract hour of publication
    df['hour'] = df[date_column].dt.hour

    # Group by hour and count publications
    hourly_count = df.groupby('hour').size().reset_index(name='publication_count')

    # Plot publication times
    plt.figure(figsize=(12, 6))
    sns.barplot(data=hourly_count, x='hour', y='publication_count', palette='viridis')
    plt.title('Publishing Times Distribution')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Publications')
    plt.xticks(range(0, 24))
    plt.grid(True)
    plt.show()

    return hourly_count
