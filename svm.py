import os
import json
import pickle
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

VECTORIZER_SAVE_PATH = 'models/svm/vectorizer.pkl'
MODEL_SAVE_PATH = 'models/svm/svm_model.pkl'

# Load data function
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
                    year = metadata.get('year') or metadata.get('date')
                    
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

# Prepare data
def prepare_data(word_count_data, metadata_list):
    vectorizer = DictVectorizer()
    X = vectorizer.fit_transform(word_count_data)
    y = [metadata['year'] for metadata in metadata_list]
    return X, y, vectorizer

# Train SVM model with Grid Search and save
def train_svm(X_train, y_train, vectorizer):
    pipeline = Pipeline([
        ('svm', SVR(kernel='rbf'))
    ])

    param_grid = {
        'svm__C': [1, 10, 100],
        'svm__gamma': ['scale', 0.01, 0.001]
    }

    grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    print("Best parameters found for SVM:", grid_search.best_params_)

    # Save best model and vectorizer
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(VECTORIZER_SAVE_PATH), exist_ok=True)
    with open(MODEL_SAVE_PATH, "wb") as model_file, open(VECTORIZER_SAVE_PATH, "wb") as vec_file:
        pickle.dump(best_model, model_file)
        pickle.dump(vectorizer, vec_file)
    print("SVM model and vectorizer saved successfully.")
    return best_model

# Main function
def main(bag_of_words_folder):
    print("Loading data...")
    word_count_data, metadata_list = load_word_counts_and_metadata(bag_of_words_folder)

    if not word_count_data or not metadata_list:
        print("No valid data found for prediction.")
        return
    
    print("Preparing data for model...")
    X, y, vectorizer = prepare_data(word_count_data, metadata_list)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    best_model = train_svm(X_train, y_train, vectorizer)

    # Evaluate the model
    predictions = best_model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print("Mean Squared Error:", mse)

    print("\nExample Predictions (True Date vs Predicted Date):")
    for true, pred in zip(y[:5], predictions[:5]):
        print(f"True Date: {true}, Predicted Date: {int(pred)}")

    # Visualize Actual vs Predicted Years
    import matplotlib.pyplot as plt
    import seaborn as sns

    min_test_year = min(y_test)
    max_test_year = max(y_test)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_test, y=predictions, alpha=0.5)
    plt.xlabel('Actual Year')
    plt.ylabel('Predicted Year')
    plt.title('Actual vs Predicted Year')
    plt.plot([min_test_year, max_test_year], [min_test_year, max_test_year], 'r--')  # Diagonal line
    plt.show()


if __name__ == "__main__":
    # Specify the correct folder path
    bag_of_words_folder = 'data/counts'
    main(bag_of_words_folder)
