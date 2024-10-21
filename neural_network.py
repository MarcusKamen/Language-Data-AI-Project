# scripts/train_model.py

import os
import pandas as pd
import json
import pickle
import re
from tqdm import tqdm

# Sklearn and TensorFlow imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Paths
CLEANED_DATA_PATH = 'data/raw_clean/'  # Path to cleaned text files
COUNTS_DATA_PATH = 'data/counts/'      # Path to word count JSON files
METADATA_PATH = 'metadata/metadata.csv'  # Path to metadata.csv
PROCESSED_DATA_PATH = 'processed_data/processed_data.csv'  # Output path

MODEL_SAVE_PATH = 'models/text_year_model.h5'
VECTORIZER_SAVE_PATH = 'models/tfidf_vectorizer.pkl'

def load_metadata(metadata_path):
    """Load metadata CSV."""
    metadata = pd.read_csv(metadata_path)
    return metadata

def load_cleaned_text(cleaned_data_path, filename):
    """Load cleaned text from a file."""
    file_path = os.path.join(cleaned_data_path, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except Exception as e:
        print(f"Error reading cleaned file {filename}: {e}")
        return None

def prepare_dataset(metadata_df, cleaned_data_path):
    """Prepare the dataset by merging metadata with cleaned text."""
    texts = []
    years = []
    valid_filenames = []

    print("Loading and merging cleaned text with metadata...")
    for index, row in tqdm(metadata_df.iterrows(), total=metadata_df.shape[0]):
        filename = row['FileName']
        year = row['Year']

        if pd.isna(filename) or pd.isna(year):
            continue  # Skip if filename or year is missing

        text = load_cleaned_text(cleaned_data_path, filename)
        if text:
            texts.append(text)
            years.append(year)
            valid_filenames.append(filename)
        else:
            print(f"Warning: Cleaned file {filename} could not be loaded.")

    # Create a new DataFrame
    data = pd.DataFrame({
        'filename': valid_filenames,
        'text': texts,
        'year': years
    })

    # Save the processed data for future reference
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    data.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Processed data saved to {PROCESSED_DATA_PATH}")

    return data

def preprocess_texts(texts):
    """Preprocess texts using TF-IDF Vectorizer."""
    print("Extracting TF-IDF features...")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')  # Adjust max_features as needed
    X = vectorizer.fit_transform(texts).toarray()
    return X, vectorizer

def build_regression_model(input_dim):
    """Build and compile a neural network for regression."""
    model = Sequential([
        Dense(512, activation='relu', input_dim=input_dim),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(1)  # Single output for regression
    ])

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])
    return model

def main():
    """Main function to train the neural network model."""
    # Load metadata
    print("Loading metadata...")
    metadata_df = load_metadata(METADATA_PATH)

    # Prepare dataset
    data = prepare_dataset(metadata_df, CLEANED_DATA_PATH)

    # Feature Extraction
    X, vectorizer = preprocess_texts(data['text'])

    # Save the TF-IDF vectorizer
    os.makedirs(os.path.dirname(VECTORIZER_SAVE_PATH), exist_ok=True)
    with open(VECTORIZER_SAVE_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"TF-IDF vectorizer saved to {VECTORIZER_SAVE_PATH}")

    # Prepare target variable
    y = data['year'].values

    # Split the data
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Optional: Scale the features (helpful for neural networks)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Save the scaler for future use
    scaler_path = '../models/scaler.pkl'
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Scaler saved to {scaler_path}")

    # Build the model
    input_dim = X_train.shape[1]
    print("Building the neural network model...")
    model = build_regression_model(input_dim)

    # Train the model
    print("Training the model...")
    history = model.fit(
        X_train, y_train,
        epochs=30,  # Adjust epochs as needed
        batch_size=128,
        validation_split=0.2,
        verbose=1
    )

    # Evaluate the model
    print("Evaluating the model on the test set...")
    loss, mae = model.evaluate(X_test, y_test, verbose=1)
    print(f"Test Mean Absolute Error: {mae}")
    print(f"Test Mean Squared Error: {loss}")

    # Make predictions
    y_pred = model.predict(X_test).flatten()

    # Visualize Actual vs Predicted Years
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.5)
    plt.xlabel('Actual Year')
    plt.ylabel('Predicted Year')
    plt.title('Actual vs Predicted Year')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')  # Diagonal line
    plt.show()

    # Save the trained model
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    model.save(MODEL_SAVE_PATH)
    print(f"Trained model saved to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    main()
