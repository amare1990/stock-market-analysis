import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_publisher_contribution(df, publisher_column):
    """
    Analyzes the contribution of each publisher in terms of the number of articles.

    Args:
        df (pd.DataFrame): Input DataFrame.
        publisher_column (str): Column containing publisher information.

    Returns:
        pd.DataFrame: Publisher contribution data (articles per publisher).
    """
    # Count the number of articles per publisher
    publisher_counts = df[publisher_column].value_counts().reset_index(name='publication_count')
    publisher_counts.columns = [publisher_column, 'publication_count']

    # Plot the contribution of publishers
    plt.figure(figsize=(12, 6))
    sns.barplot(data=publisher_counts.head(10), x=publisher_column, y='publication_count', palette='viridis')
    plt.title('Top 10 Publishers by Publication Count')
    plt.xlabel('Publisher')
    plt.ylabel('Number of Publications')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

    return publisher_counts

def analyze_publisher_domains(df, publisher_column):
    """
    Identifies unique domains in publisher names (email addresses).

    Args:
        df (pd.DataFrame): Input DataFrame.
        publisher_column (str): Column containing publisher information (email addresses).

    Returns:
        pd.DataFrame: Domain frequency data.
    """
    # Extract domains from email addresses (assuming publisher is an email)
    df['publisher_domain'] = df[publisher_column].str.split('@').str[1]

    # Count occurrences of each domain
    domain_counts = df['publisher_domain'].value_counts().reset_index(name='publication_count')
    domain_counts.columns = ['domain', 'publication_count']

    # Plot domain contributions
    plt.figure(figsize=(12, 6))
    sns.barplot(data=domain_counts.head(10), x='domain', y='publication_count', palette='viridis')
    plt.title('Top 10 Domains by Publisher Count')
    plt.xlabel('Domain')
    plt.ylabel('Number of Publications')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

    return domain_counts
