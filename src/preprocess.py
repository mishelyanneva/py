import re
from typing import List, Dict, Any, Optional, Union
import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

STOP_WORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(description: str) -> str:

    description = re.sub(r'PAYPAL \*', '', description, flags=re.IGNORECASE)
    description = re.sub(r'^(WWW\.|HTTP://|HTTPS://)', '', description, flags=re.IGNORECASE)
    description = re.sub(r'[^a-zA-Z0-9\s]', '', description)
    description = re.sub(r'\s+', ' ', description).strip()
    return description

def normalize_text(description: str) -> str:

    tokens = description.lower().split()
    tokens = [word for word in tokens if word not in STOP_WORDS]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

def feature_extraction(texts: List[str], max_features: int = 500):

    vectorizer = TfidfVectorizer(max_features=max_features)
    features = vectorizer.fit_transform(texts)
    return features, vectorizer.get_feature_names_out()

def preprocess_text(description: str) -> str:

    cleaned = clean_text(description)
    normalized = normalize_text(cleaned)
    return normalized

def _convert_to_datetime(series: pd.Series) -> pd.Series:

    try:
        return pd.to_datetime(series, errors='coerce')
    except Exception as e:
        print(f"Datetime conversion warning: {e}")
        return series

class FlexibleTableProcessor:
    def __init__(self,
                 required_columns: Optional[List[str]] = None,
                 date_columns: Optional[List[str]] = None,
                 numeric_columns: Optional[List[str]] = None):

        self.required_columns = required_columns or []
        self.date_columns = date_columns or []
        self.numeric_columns = numeric_columns or []

    def validate_table_structure(self, df: pd.DataFrame) -> Dict[str, Any]:

        analysis = {
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'missing_required_columns': [
                col for col in self.required_columns if col not in df.columns
            ],
            'column_types': df.dtypes.to_dict()
        }
        return analysis

    def preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:

        # Create a copy to avoid modifying original
        processed_df = df.copy()

        # Handle date columns
        for col in self.date_columns:
            if col in processed_df.columns:
                processed_df[col] = _convert_to_datetime(processed_df[col])

        # Handle numeric columns
        for col in self.numeric_columns:
            if col in processed_df.columns:
                processed_df[col] = self._convert_to_numeric(processed_df[col])

        # Fill missing columns if required
        for col in self.required_columns:
            if col not in processed_df.columns:
                processed_df[col] = np.nan

        return processed_df

    @staticmethod
    def _convert_to_numeric(series: pd.Series) -> pd.Series:
        def parse_numeric(value: Any) -> Union[float, np.nan]:
            if isinstance(value, (int, float)):
                return value
            if isinstance(value, str):
                value = re.sub(r'[^\d.-]', '', value)
                try:
                    return float(value)
                except ValueError:
                    return np.nan
            return np.nan

        return series.apply(parse_numeric)

    @staticmethod
    def handle_column_mapping(df: pd.DataFrame, column_map: Dict[str, str]) -> pd.DataFrame:
        return df.rename(columns=column_map)

    @staticmethod
    def detect_delimiter(file_path: str) -> str:
        with open(file_path, 'r') as f:
            first_line = f.readline().strip()

        delimiters = [',', ';', '\t', '|']
        for delimiter in delimiters:
            if delimiter in first_line:
                return delimiter

        return ','

    def load_flexible_table(self,
                            file_path: str,
                            delimiter: Optional[str] = None) -> pd.DataFrame:

        if delimiter is None:
            delimiter = self.detect_delimiter(file_path)

        try:
            df = pd.read_csv(file_path, delimiter=delimiter)
            return self.preprocess_dataframe(df)
        except Exception as e:
            print(f"Error loading file: {e}")
            return pd.DataFrame()

    @staticmethod
    def calculate_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
        # Ensure 'Date' column is datetime format
        if 'Date' not in df.columns or 'Amount' not in df.columns:
            raise ValueError("Both 'Amount' and 'Date' columns are required for summary calculation.")

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Extract Year-Month for grouping
        df['Month'] = df['Date'].dt.to_period('M')

        # Calculate total income and expenses
        monthly_summary = df.groupby('Month').agg(
            total_income=pd.NamedAgg(column='Amount', aggfunc=lambda x: x[x > 0].sum()),
            total_expenses=pd.NamedAgg(column='Amount', aggfunc=lambda x: x[x < 0].sum()),
            balance=pd.NamedAgg(column='Amount', aggfunc='sum')
        ).reset_index()

        monthly_summary.fillna(0, inplace=True)

        return monthly_summary