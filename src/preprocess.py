import re
import os
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK resources
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Stopwords and Lemmatizer setup
STOP_WORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def clean_text(description: str) -> str:
    """
    Clean text by removing unnecessary characters and standardizing format

    Args:
        description (str): Input text description

    Returns:
        str: Cleaned text
    """
    description = re.sub(r'PAYPAL \*', '', description, flags=re.IGNORECASE)
    description = re.sub(r'^(WWW\.|HTTP://|HTTPS://)', '', description, flags=re.IGNORECASE)
    description = re.sub(r'[^a-zA-Z0-9\s]', '', description)
    description = re.sub(r'\s+', ' ', description).strip()
    return description


def normalize_text(description: str) -> str:
    """
    Normalize text by lowercasing, removing stopwords, and lemmatizing

    Args:
        description (str): Input text description

    Returns:
        str: Normalized text
    """
    tokens = description.lower().split()
    tokens = [word for word in tokens if word not in STOP_WORDS]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)


def feature_extraction(texts: List[str], max_features: int = 500):
    """
    Extract features using TF-IDF vectorization

    Args:
        texts (List[str]): List of text descriptions
        max_features (int, optional): Maximum number of features. Defaults to 500.

    Returns:
        Tuple of feature matrix and feature names
    """
    vectorizer = TfidfVectorizer(max_features=max_features)
    features = vectorizer.fit_transform(texts)
    return features, vectorizer.get_feature_names_out()


def preprocess_text(description: str) -> str:
    """
    Complete text preprocessing pipeline

    Args:
        description (str): Input text description

    Returns:
        str: Fully preprocessed text
    """
    cleaned = clean_text(description)
    normalized = normalize_text(cleaned)
    return normalized


class FlexibleTableProcessor:
    def __init__(self,
                 required_columns: Optional[List[str]] = None,
                 date_columns: Optional[List[str]] = None,
                 numeric_columns: Optional[List[str]] = None):
        """
        Initialize the table processor with flexible configuration

        Args:
            required_columns (list, optional): Columns that must be present
            date_columns (list, optional): Columns to be converted to datetime
            numeric_columns (list, optional): Columns to be converted to numeric
        """
        self.required_columns = required_columns or []
        self.date_columns = date_columns or []
        self.numeric_columns = numeric_columns or []

    def validate_table_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate and analyze the table structure

        Args:
            df (pd.DataFrame): Input dataframe

        Returns:
            Dict with table structure analysis
        """
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
        """
        Preprocess dataframe with flexible handling

        Args:
            df (pd.DataFrame): Input dataframe

        Returns:
            Preprocessed dataframe
        """
        # Create a copy to avoid modifying original
        processed_df = df.copy()

        # Handle date columns
        for col in self.date_columns:
            if col in processed_df.columns:
                processed_df[col] = self._convert_to_datetime(processed_df[col])

        # Handle numeric columns
        for col in self.numeric_columns:
            if col in processed_df.columns:
                processed_df[col] = self._convert_to_numeric(processed_df[col])

        # Fill missing columns if required
        for col in self.required_columns:
            if col not in processed_df.columns:
                processed_df[col] = np.nan

        return processed_df

    def _convert_to_datetime(self, series: pd.Series) -> pd.Series:
        """
        Convert series to datetime with flexible parsing

        Args:
            series (pd.Series): Input series

        Returns:
            Datetime series
        """
        try:
            return pd.to_datetime(series, errors='coerce')
        except Exception as e:
            print(f"Datetime conversion warning: {e}")
            return series

    def _convert_to_numeric(self, series: pd.Series) -> pd.Series:
        """
        Convert series to numeric with flexible parsing

        Args:
            series (pd.Series): Input series

        Returns:
            Numeric series
        """

        def parse_numeric(value: Any) -> Union[float, np.nan]:
            if isinstance(value, (int, float)):
                return value

            if isinstance(value, str):
                # Remove currency symbols and commas
                value = re.sub(r'[^\d.-]', '', value)
                try:
                    return float(value)
                except ValueError:
                    return np.nan

            return np.nan

        return series.apply(parse_numeric)

    def handle_column_mapping(self,
                              df: pd.DataFrame,
                              column_map: Dict[str, str]) -> pd.DataFrame:
        """
        Rename columns based on a mapping dictionary

        Args:
            df (pd.DataFrame): Input dataframe
            column_map (dict): Mapping of old column names to new column names

        Returns:
            Dataframe with renamed columns
        """
        return df.rename(columns=column_map)

    def detect_delimiter(self, file_path: str) -> str:
        """
        Automatically detect delimiter for CSV files

        Args:
            file_path (str): Path to the CSV file

        Returns:
            Detected delimiter
        """
        with open(file_path, 'r') as f:
            first_line = f.readline().strip()

        delimiters = [',', ';', '\t', '|']
        for delimiter in delimiters:
            if delimiter in first_line:
                return delimiter

        return ','  # default to comma

    def load_flexible_table(self,
                            file_path: str,
                            delimiter: Optional[str] = None) -> pd.DataFrame:
        """
        Load table with flexible delimiter detection

        Args:
            file_path (str): Path to the file
            delimiter (str, optional): Predefined delimiter

        Returns:
            Loaded dataframe
        """
        if delimiter is None:
            delimiter = self.detect_delimiter(file_path)

        try:
            df = pd.read_csv(file_path, delimiter=delimiter)
            return self.preprocess_dataframe(df)
        except Exception as e:
            print(f"Error loading file: {e}")
            return pd.DataFrame()