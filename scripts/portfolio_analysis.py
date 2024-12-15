import os
import pandas as pd
import yfinance as yf
import pyfolio as pf
from pypfopt import expected_returns, risk_models, EfficientFrontier
import matplotlib.pyplot as plt

class PortfolioOptimizer:
    def __init__(self, tickers, start_date, end_date, output_folder):
        """
        Initialize PortfolioOptimizer with tickers, date range, and output folder for saving plots.

        :param tickers: List of tickers (e.g., ['AAPL', 'GOOGL', 'MSFT'])
        :param start_date: Start date for data download (e.g., '2020-01-01')
        :param end_date: End date for data download (e.g., '2021-01-01')
        :param output_folder: Directory to save output plots (e.g., './plots')
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.output_folder = output_folder
        self.data = self.download_data()

    def download_data(self):
        """
        Download historical stock data for the given tickers and date range using Yahoo Finance.

        :return: DataFrame with adjusted close prices for the tickers.
        """
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date)['Adj Close']
        return data

    def calculate_portfolio_weights(self):
        """
        Calculate the optimal portfolio weights using PyPortfolioOpt.

        :return: Dictionary of portfolio weights.
        """
        # Step 1: Calculate expected returns and the covariance matrix of returns
        mu = expected_returns.mean_historical_return(self.data)
        S = risk_models.sample_cov(self.data)

        # Step 2: Use Efficient Frontier to calculate the optimal weights
        ef = EfficientFrontier(mu, S)
        weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()

        return cleaned_weights

    def calculate_performance(self, weights):
        """
        Calculate portfolio performance using the calculated weights.

        :param weights: Dictionary of portfolio weights
        :return: Dictionary of performance metrics.
        """
        # Convert weights to a pandas series
        weights_series = pd.Series(weights)

        # Calculate portfolio returns using the asset returns and weights
        portfolio_returns = (self.data.pct_change() * weights_series.T).sum(axis=1)

        # Calculate performance metrics using PyFolio
        perf = pf.timeseries.perf_stats(portfolio_returns)

        return perf

    def plot_portfolio_returns(self, weights):
        """
        Plot portfolio returns using PyFolio.

        :param weights: Dictionary of portfolio weights
        """
        # Convert weights to pandas series
        weights_series = pd.Series(weights)

        # Calculate portfolio returns
        portfolio_returns = (self.data.pct_change() * weights_series.T).sum(axis=1)

        # Plot portfolio returns using PyFolio
        fig, ax = plt.subplots(figsize=(10, 6))
        pf.plot_returns(portfolio_returns, ax=ax)

        # Save the plot to the specified output folder
        if not os.path.exists(self.output_folder):
           os.makedirs(self.output_folder)

        plot_filename = os.path.join(self.output_folder, 'portfolio_returns.png')
        plt.savefig(plot_filename)
        plt.close(fig)
        print(f"Plot saved at {plot_filename}")
