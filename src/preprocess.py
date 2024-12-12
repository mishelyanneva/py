import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('stopwords')
nltk.download('wordnet')


STOP_WORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(description):
    # Remove unnecessary characters, URLs, and special symbols
    description = re.sub(r'PAYPAL \*', '', description, flags=re.IGNORECASE)
    description = re.sub(r'^(WWW\.|HTTP://|HTTPS://)', '', description, flags=re.IGNORECASE)
    description = re.sub(r'[^a-zA-Z0-9\s]', '', description)
    description = re.sub(r'\s+', ' ', description).strip()
    return description

def normalize_text(description):

    tokens = description.lower().split()
    tokens = [word for word in tokens if word not in STOP_WORDS]

    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

def feature_extraction(texts):
    # Use TF-IDF to extract features
    vectorizer = TfidfVectorizer(max_features=500)
    features = vectorizer.fit_transform(texts)
    return features, vectorizer.get_feature_names_out()

def preprocess_text(description):
    cleaned = clean_text(description)
    normalized = normalize_text(cleaned)
    return normalized
