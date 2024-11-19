import os
import pandas as pd
import pickle
import re
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.regularizers import l2
from tensorflow.keras.losses import Huber
from tensorflow.keras.callbacks import EarlyStopping
from scipy.sparse import save_npz, load_npz
from scipy.sparse import csr_matrix
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.optimizers import Adam

# Paths
CLEANED_DATA_PATH = 'data/raw_clean/'  # Path to cleaned text files
METADATA_PATH = 'metadata/metadata.csv'  # Path to metadata.csv
NO_FIRST_SENTENCE_PATH = 'metadata/nofirstsentence.csv'  # Path to nofirstsentence.csv
PROCESSED_DATA_PATH = 'processed_data/processed_data.csv'  # Output path

MODEL_SAVE_PATH = 'models/text_year_model.h5'
VECTORIZER_SAVE_PATH = 'models/tfidf_vectorizer.pkl'
SCALER_SAVE_PATH = 'models/scaler.pkl'
TFIDF_SPARSE_MATRIX_PATH = 'processed_data/tfidf_sparse.npz'  # Sparse matrix path

def load_metadata(metadata_path, no_first_sentence_path):
    """Load metadata from multiple CSV files and combine them."""
    metadata = pd.read_csv(metadata_path)
    no_first_sentence = pd.read_csv(no_first_sentence_path)
    combined_metadata = pd.concat([metadata, no_first_sentence], ignore_index=True)
    return combined_metadata

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
    texts, years, valid_filenames = [], [], []

    print("Loading and merging cleaned text with metadata...")
    for index, row in tqdm(metadata_df.iterrows(), total=metadata_df.shape[0]):
        filename = row['FileName']
        year = row['Year']

        if pd.isna(filename) or pd.isna(year):
            continue  # Skip if filename or year is missing

        text = load_cleaned_text(cleaned_data_path, filename)
        if text:
            texts.append(" ".join(text.split()[:200]))  # Limit each document to first 200 words
            years.append(year)
            valid_filenames.append(filename)
        else:
            print(f"Warning: Cleaned file {filename} could not be loaded.")

    data = pd.DataFrame({'filename': valid_filenames, 'text': texts, 'year': years})
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    data.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Processed data saved to {PROCESSED_DATA_PATH}")
    return data

def preprocess_texts(texts):
    """Preprocess texts using TF-IDF Vectorizer with trigrams."""
    print("Extracting TF-IDF features with trigrams...")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 3), sublinear_tf=True)
    X = vectorizer.fit_transform(texts)
    save_npz(TFIDF_SPARSE_MATRIX_PATH, X)
    return X, vectorizer

def build_regression_model(input_dim):
    """Build and compile a neural network for regression with L2 regularization, BatchNorm, and Huber loss."""
    model = Sequential([
        Dense(512, activation='relu', input_dim=input_dim, kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        Dropout(0.3),  # Reduced Dropout
        Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        Dropout(0.3),
        Dense(128, activation='relu', kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        Dropout(0.2),  # Reduced Dropout
        Dense(1)  # Single output for regression
    ])
    optimizer = Adam(learning_rate=0.001)  # Tuned learning rate
    model.compile(optimizer=optimizer, loss=Huber(), metrics=['mean_absolute_error'])
    return model

def main():
    """Main function to train the neural network model."""
    print("Loading metadata...")
    metadata_df = load_metadata(METADATA_PATH, NO_FIRST_SENTENCE_PATH)

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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Optional: Scale the features (helpful for neural networks)
    scaler = StandardScaler(with_mean=False)  # for sparse matrix compatibility
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Save the scaler for future use
    os.makedirs(os.path.dirname(SCALER_SAVE_PATH), exist_ok=True)
    with open(SCALER_SAVE_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Scaler saved to {SCALER_SAVE_PATH}")

    # Build the model
    input_dim = X_train.shape[1]
    print("Building the neural network model...")
    model = build_regression_model(input_dim)

    # Early stopping callback
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    # Train the model with early stopping
    print("Training the model...")
    history = model.fit(
        X_train, y_train,
        epochs=120,  # Increased epochs for potentially longer training
        batch_size=64,  # Smaller batch size for better generalization
        validation_split=0.2,
        verbose=1,
        callbacks=[early_stopping]
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
