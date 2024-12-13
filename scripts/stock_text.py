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

def extract_topics(df, column, num_topics=5, num_keywords=10):
    """
    Extracts topics from text data using Latent Dirichlet Allocation (LDA).

    Args:
        df (pd.DataFrame): The input DataFrame.
        column (str): The column containing text data.
        num_topics (int): Number of topics to extract.
        num_keywords (int): Number of keywords to display per topic.

    Returns:
        dict: A dictionary of topics with their keywords.
    """
    # Clean the text data
    df['cleaned_text'] = df[column].apply(clean_text)

    # Vectorize the text data
    vectorizer = CountVectorizer(stop_words='english', max_df=0.9, min_df=2)
    text_vectors = vectorizer.fit_transform(df['cleaned_text'])

    # Apply LDA for topic modeling
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(text_vectors)

    topics = {}
    for idx, topic in enumerate(lda.components_):
        top_keywords = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-num_keywords:]]
        topics[f"Topic {idx + 1}"] = top_keywords

    return topics

