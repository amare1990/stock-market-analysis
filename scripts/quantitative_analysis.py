import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import talib as ta
import yfinance as yf
from pynance import data as pynance_data

class stock_quantitative_analyzer:
    def __init__(self, ticker, start_date, end_date, output_folder):
        """
        Initializes the StockAnalysisVisualizer class.

        Args:
            ticker (str): Stock symbol (e.g., 'AAPL').
            start_date (str): Start date for fetching data (format: 'YYYY-MM-DD').
            end_date (str): End date for fetching data (format: 'YYYY-MM-DD').
            output_folder (str): Folder where visualizations will be saved.
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.output_folder = output_folder

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Fetch stock data using yfinance
        self.stock_data = yf.download(ticker, start=start_date, end=end_date)
        self.stock_data['Date'] = self.stock_data.index

    def calculate_indicators(self):
        """
        Calculates technical indicators using TA-Lib.
        """
        # Simple Moving Average (SMA)
        self.stock_data['SMA-20'] = ta.SMA(self.stock_data['Close'], timeperiod=20)

        # Relative Strength Index (RSI)
        self.stock_data['RSI_14'] = ta.RSI(self.stock_data['Close'], timeperiod=14)

        # Moving Average convergence Divergence (MACD)
        self.stock_data['MACD'], self.stock_data['MACD_signal'], self.stock_data['MACD_hist'] = ta.MACD(
            self.stock_data['Close'], fastperiod=12, slowperiod=26, signalperiod=9
        )


    def plot_stock_data(self):
        # Drop rows with NaN values in either 'Close' or 'SMA_20'
        valid_data = self.stock_data.dropna(subset=['Close', 'SMA-20'])

        # Plot using Plotly Express
        fig = px.line(
            valid_data,
            x=valid_data.index,
            y=['Close', 'SMA-20'],
            title="Stock Price with Simple Moving Average"
        )
        fig.show()

        if not os.path.exists(self.output_folder):
             print(f"Output folder '{self.output_folder}' does not exist. Creating it.")
             os.makedirs(self.output_folder)

        file_path = os.path.join(self.output_folder, f'{self.ticker}_stock_sma.png')
        plt.savefig(f"Plot saved at {file_path}")

        plt.close()

    # Plot the effect of RSI over stock price
    def plot_rsi(self):
        # Drop rows with NaN values in either 'Close' or 'SMA_20'
        valid_data = self.stock_data.dropna(subset=['Close', 'RSI_14'])

        # Plot using Plotly Express
        fig = px.line(
            valid_data,
            x=valid_data.index,
            y=['Close', 'RSI_14'],
            title="Relative Strength Index (RSI)"
        )
        fig.show()

        if not os.path.exists(self.output_folder):
             print(f"Output folder '{self.output_folder}' does not exist. Creating it.")
             os.makedirs(self.output_folder)

        file_path = os.path.join(self.output_folder, f'{self.ticker}_stock_rsi.png')
        plt.savefig(f"Plot saved at {file_path}")

        plt.close()

    # Plot the effect of RSI over stock price
    def plot_macd(self):
        # Drop rows with NaN values in either 'Close' or 'SMA_20'
        valid_data = self.stock_data.dropna(subset=['Close', 'MACD'])

        # Plot using Plotly Express
        fig = px.line(
            valid_data,
            x=valid_data.index,
            y=['Close', 'MACD', 'MACD_signal', 'MACD_hist'],
            title="Moving Average Convergence Divergence (MACD), MACD_signal, MACD_hist"
        )
        fig.show()

        if not os.path.exists(self.output_folder):
             print(f"Output folder '{self.output_folder}' does not exist. Creating it.")
             os.makedirs(self.output_folder)

        file_path = os.path.join(self.output_folder, f'{self.ticker}_stock_macd.png')
        plt.savefig(f"Plot saved at {file_path}")

        plt.close()

    def plot_indicators(self):
        # Drop rows with NaN values
        valid_data = self.stock_data.dropna(subset=['Close', 'SMA-20', 'RSI_14', 'MACD', 'MACD_signal', 'MACD_hist'])

        # Create figure
        fig = go.Figure()

        # Add the stock price (Close)
        fig.add_trace(go.Scatter(x=valid_data.index, y=valid_data['Close'], mode='lines', name='Close Price'))

        # Add indicators
        fig.add_trace(go.Scatter(x=valid_data.index, y=valid_data['SMA-20'], mode='lines', name='SMA-20'))
        fig.add_trace(go.Scatter(x=valid_data.index, y=valid_data['RSI_14'], mode='lines', name='RSI-14'))
        fig.add_trace(go.Scatter(x=valid_data.index, y=valid_data['MACD'], mode='lines', name='MACD'))
        fig.add_trace(go.Scatter(x=valid_data.index, y=valid_data['MACD_signal'], mode='lines', name='MACD Signal'))
        fig.add_trace(go.Scatter(x=valid_data.index, y=valid_data['MACD_hist'], mode='lines', name='MACD Histogram'))

        # Update layout for readability
        fig.update_layout(
            title="Effect of Financial Indicators on Stock Price",
            xaxis_title="Date",
            yaxis_title="Values",
            legend_title="Indicators",
            template="plotly_white"
        )

        # Show plot
        fig.show()

        # Save plot as a static image (optional, ensure Kaleido is installed)
        if not os.path.exists(self.output_folder):
            print(f"Output folder '{self.output_folder}' does not exist. Creating it.")
            os.makedirs(self.output_folder)

        file_path = os.path.join(self.output_folder, f'{self.ticker}_stock_fin_indicators.png')
        fig.write_image(file_path)
        print(f"Plot saved at {file_path}")



