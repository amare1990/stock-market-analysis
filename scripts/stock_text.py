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
