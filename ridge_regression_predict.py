import os
import json
from sklearn.linear_model import Ridge
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import pickle

VECTORIZER_SAVE_PATH = 'models/ridge/vectorizer.pkl'
MODEL_SAVE_PATH = 'models/ridge/ridge_model.pkl'

def load_word_counts_and_metadata(folder):
    word_count_data = []
    metadata_list = []
    
    print("Reading files from:", folder)
    
    for filename in os.listdir(folder):
        if filename.endswith('_counts.json'):
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    metadata = data.get('metadata', {})
                    
                    # Flexible year extraction
                    year = metadata.get('year') or metadata.get('year') or metadata.get('date')
                    
                    if year is None:
                        print(f"Skipped {filename}: Invalid year None")
                        continue
                    
                    try:
                        year = int(year)  # Convert to integer if possible
                        if not (1000 <= year <= 2000):
                            print(f"Skipped {filename}: year out of range {year}")
                            continue
                    except (ValueError, TypeError):
                        print(f"Skipped {filename}: Invalid year {year}")
                        continue
                    
                    word_count = data.get('word_counts')
                    if word_count is None:
                        print(f"Skipped {filename}: Missing word_counts")
                        continue
                    
                    word_count_data.append(word_count)
                    metadata_list.append({'year': year})
                    print(f"Included {filename} with year {year}")

            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error reading {filename}: {e}")

    if not word_count_data:
        print("No valid data found for prediction.")
    
    return word_count_data, metadata_list


def prepare_data(word_count_data, metadata_list):
    vectorizer = DictVectorizer()
    X = vectorizer.fit_transform(word_count_data)
    y = [metadata['year'] for metadata in metadata_list]
    return X, y, vectorizer


def main(bag_of_words_folder):
    print("Loading data...")
    word_count_data, metadata_list = load_word_counts_and_metadata(bag_of_words_folder)

    if not word_count_data or not metadata_list:
        print("No valid data found for prediction.")
        return
    
    print("Preparing data for regression model...")
    X, y, vectorizer = prepare_data(word_count_data, metadata_list)

    # Save the vectorizer for future use
    os.makedirs(os.path.dirname(VECTORIZER_SAVE_PATH), exist_ok=True)
    with open(VECTORIZER_SAVE_PATH, 'wb') as file:
        pickle.dump(vectorizer, file)
    print(f"Vectorizer saved to {VECTORIZER_SAVE_PATH}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = Ridge()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print("Mean Squared Error:", mse)
    # print("Sample predictions:", predictions[:5])
    print("\nExample Predictions (True Date vs Predicted Date):")
    for true, pred in zip(y[:5], predictions[:5]):
        print(f"True Date: {true}, Predicted Date: {int(pred)}")

    # Save the trained model
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    with open(MODEL_SAVE_PATH, 'wb') as file:
        pickle.dump(model, file)
    print(f"Trained model saved to {MODEL_SAVE_PATH}")


if __name__ == "__main__":
    bag_of_words_folder = 'data/counts'  # Specify the correct folder path
    main(bag_of_words_folder)
