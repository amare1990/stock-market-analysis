import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re
import nltk
from nltk.corpus import stopwords

# Add NLTK data path
nltk.data.path.append('/home/am/corpus/')
print(f"NLTK data path: {nltk.data.path}")

# Load stopwords
try:
    stop_words = set(stopwords.words('english'))
    print(f"Number of stopwords: {len(stop_words)}")
except LookupError as e:
    print(f"Error loading stopwords: {e}")


def clean_text(text):
    """
    Cleans text by removing special characters, numbers, and extra spaces.
    """
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def perform_sentiment_analysis(df, column):
    """
    Performs sentiment analysis on a specified column of a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column (str): The column containing text data.

    Returns:
        pd.DataFrame: A DataFrame with sentiment scores and labels.
    """
    sentiments = df[column].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['sentiment_score'] = sentiments
    df['sentiment_label'] = df['sentiment_score'].apply(
        lambda score: 'positive' if score > 0 else 'negative' if score < 0 else 'neutral'
    )
    return df
