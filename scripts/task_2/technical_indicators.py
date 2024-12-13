import talib
import pandas as pd

def calculate_technical_indicators(df):
    """
    Calculate technical indicators (SMA, RSI, MACD) using TA-Lib and add them to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame containing at least a 'Close' column.

    Returns:
        pd.DataFrame: DataFrame with new columns for SMA, RSI, and MACD indicators.
    """
    if 'Close' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'Close' column.")

    df['Close'] = (df['Close'] - df['Close'].mean()) / df['Close'].std()

    # Calculate SMA (Simple Moving Average)
    df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)

    # Calculate RSI (Relative Strength Index)
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)

    # Calculate MACD (Moving Average Convergence Divergence)
    macd, macd_signal, macd_hist = talib.MACD(
        df['Close'], fastperiod=12, slowperiod=26, signalperiod=9
    )
    df['MACD'] = macd
    df['MACD_signal'] = macd_signal
    df['MACD_hist'] = macd_hist

    return df
