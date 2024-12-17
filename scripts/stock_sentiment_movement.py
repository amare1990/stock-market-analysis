import pandas as pd
import yfinance as yf
from datetime import datetime
from textblob import TextBlob
import os
import re

class stock_news_movement_analysis:
    def __init__(self, tickers, start_date, end_date, output_folder):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.output_folder = output_folder
        self.stock_data = None
        self.news_data = None
        self.merged_data = None

    def download_stock_data(self):
        """Download stock data from Yahoo Finance."""
        # Download stock data for provided tickers
        self.stock_data = yf.download(self.tickers, start=self.start_date, end=self.end_date)

        # Reset the index to bring 'Date' into a column
        self.stock_data.reset_index(inplace=True)

        # Ensure 'Date' is in datetime format
        self.stock_data['Date'] = pd.to_datetime(self.stock_data['Date'])

        print(f"Stock data for {self.tickers} from {self.start_date} to {self.end_date} downloaded successfully.")

    def load_news_data(self, news_file):
        """Load news data from a CSV file."""
        # Load news data
        self.news_data = pd.read_csv(news_file)
        self.news_data = self.news_data[self.news_data['stock'] == self.tickers]
        self.news_data.rename(columns={'date': 'Date'}, inplace=True)  # Rename 'date' to 'Date'

        # Convert 'Date' to datetime
        try:
            self.news_data['Date'] = pd.to_datetime(self.news_data['Date'], format='mixed', errors='coerce')
            self.news_data.dropna(subset=['Date'], inplace=True)  # Drop rows with invalid dates
        except Exception as e:
            raise ValueError(f"Error parsing dates in news data: {e}")

        print("News data loaded successfully.")

    def clean_data(self):
        """Clean and validate data."""

        # Drop unnecessary columns from stock_data and news_data
        if 'Unnamed: 0' in self.stock_data.columns:
            self.stock_data.drop(columns=['Unnamed: 0'], inplace=True)

        if 'Unnamed: 0' in self.news_data.columns:
            self.news_data.drop(columns=['Unnamed: 0'], inplace=True)
            # Flatten multi-level columns if necessary
            if isinstance(self.stock_data.columns, pd.MultiIndex):
                self.stock_data.columns = [' '.join(col).strip() for col in self.stock_data.columns.values]
                # Remove "AAPL" from column names using a regular expression
                self.stock_data.columns = [re.sub(r'\s*AAPL$', '', col) for col in self.stock_data.columns]


        # Convert 'Date' column to datetime if it exists
        if 'Date' in self.stock_data.columns:
            self.stock_data['Date'] = pd.to_datetime(self.stock_data['Date'], errors='coerce')
        # Convert 'Date' column to datetime if it exists
        if 'Date' in self.news_data.columns:
            self.news_data['Date'] = pd.to_datetime(self.news_data['Date'], errors='coerce')

        print("Data cleaning completed. Stock and news data are ready for analysis.")


    def merge_data(self):
      """Normalize and merge stock and news data."""
      # Ensure 'Date' in news_data is a datetime object

      self.stock_data['Date'] = self.stock_data['Date'].dt.date
      # Ensure the 'Date' in news_data is in the correct format

      self.news_data['Date'] = self.news_data['Date'].dt.date

      # Merge the stock data and news data on 'Date'
      self.merged_data = pd.merge(self.news_data, self.stock_data, on='Date', how='inner')

      print(f"Merged data contains {len(self.merged_data)} rows.")



    def save_data(self):
        """Save the merged data to the output folder."""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        merged_data_path = os.path.join(self.output_folder, 'merged_stock_news_data.csv')
        self.merged_data.to_csv(merged_data_path, index=False)
        print(f"Merged data saved to {merged_data_path}.")

    # Sentiment analysis
    def perform_sentiment_analysis(self):
        """Apply sentiment analysis to news headlines."""
        def get_sentiment(text):
            analysis = TextBlob(text)
            return analysis.sentiment.polarity

        self.merged_data['Sentiment'] = self.merged_data['headline'].apply(get_sentiment)

    # Calculate Daily Stock Returns
    def compute_daily_returns(self):
        """Calculate daily stock returns."""
        self.merged_data['Daily_Return'] = self.merged_data['Close'].pct_change()

    def compute_correlation(self):
        """Compute correlation between sentiment and daily stock returns."""
        # Aggregate sentiment scores
        daily_sentiment = self.merged_data.groupby('Date')['Sentiment'].mean()

        # Calculate correlation
        correlation = daily_sentiment.corr(self.merged_data['Daily_Return'])
        print(f"Pearson correlation between sentiment and daily stock returns: {correlation}")
        return correlation
