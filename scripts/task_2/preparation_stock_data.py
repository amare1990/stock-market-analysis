import pandas as pd

def prepare_stock_data(file_path):
    """
    Loads and prepares stock data for analysis.

    Args:
        file_path (str): Path to the CSV file containing stock data.

    Returns:
        pd.DataFrame: A prepared DataFrame with 'Date' as the index.
    """

    file_path = "/home/am/Documents/Software Development/10_Academy Training/week1/Data/yfinance_data/AAPL_historical_data.csv"
    # Load stock data
    df = pd.read_csv(file_path)

    # Ensure necessary columns are present
    required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing necessary columns: {missing_columns}")

    # Convert date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Handle missing values (if any)
    df.dropna(inplace=True)

    return df
