import os
import pandas as pd
import matplotlib.pyplot as plt

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

