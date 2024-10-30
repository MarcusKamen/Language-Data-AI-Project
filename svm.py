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

# Train Ridge Regression model and save
def train_ridge_regression(X_train, y_train, vectorizer):
    model = Ridge()
    model.fit(X_train, y_train)
    
    # Save model and vectorizer
    with open("ridge_regression_model.pkl", "wb") as model_file, open("vectorizer.pkl", "wb") as vec_file:
        pickle.dump(model, model_file)
        pickle.dump(vectorizer, vec_file)
    print("Ridge Regression model and vectorizer saved successfully.")

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
    with open("svm_model.pkl", "wb") as model_file, open("vectorizer.pkl", "wb") as vec_file:
        pickle.dump(best_model, model_file)
        pickle.dump(vectorizer, vec_file)
    print("SVM model and vectorizer saved successfully.")

# Main function
def main(bag_of_words_folder, model_type="ridge"):
    print("Loading data...")
    word_count_data, metadata_list = load_word_counts_and_metadata(bag_of_words_folder)

    if not word_count_data or not metadata_list:
        print("No valid data found for prediction.")
        return
    
    print("Preparing data for model...")
    X, y, vectorizer = prepare_data(word_count_data, metadata_list)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_type == "ridge":
        train_ridge_regression(X_train, y_train, vectorizer)
    elif model_type == "svm":
        train_svm(X_train, y_train, vectorizer)
    else:
        print("Unknown model type specified. Choose 'ridge' or 'svm'.")

# Specify the correct folder path
bag_of_words_folder = 'data/counts'
main(bag_of_words_folder, model_type="ridge")









# import os
# import json
# import numpy as np
# from sklearn.feature_extraction import DictVectorizer
# from sklearn.svm import SVR
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.pipeline import Pipeline

# # Load word counts and metadata as per your logic
# def load_word_counts_and_metadata(folder):
#     word_count_data = []
#     metadata_list = []
    
#     print("Reading files from:", folder)
    
#     for filename in os.listdir(folder):
#         if filename.endswith('_counts.json'):
#             file_path = os.path.join(folder, filename)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     data = json.load(file)
#                     metadata = data.get('metadata', {})
                    
#                     # Flexible year extraction
#                     year = metadata.get('year') or metadata.get('date')
                    
#                     if year is None:
#                         print(f"Skipped {filename}: Invalid year None")
#                         continue
                    
#                     try:
#                         year = int(year)  # Convert to integer if possible
#                         if not (1000 <= year <= 2000):
#                             print(f"Skipped {filename}: year out of range {year}")
#                             continue
#                     except (ValueError, TypeError):
#                         print(f"Skipped {filename}: Invalid year {year}")
#                         continue
                    
#                     word_count = data.get('word_counts')
#                     if word_count is None:
#                         print(f"Skipped {filename}: Missing word_counts")
#                         continue
                    
#                     word_count_data.append(word_count)
#                     metadata_list.append({'year': year})
#                     print(f"Included {filename} with year {year}")

#             except (json.JSONDecodeError, KeyError) as e:
#                 print(f"Error reading {filename}: {e}")

#     if not word_count_data:
#         print("No valid data found for prediction.")
    
#     return word_count_data, metadata_list

# # Prepare data for SVM
# def prepare_data(word_count_data, metadata_list):
#     vectorizer = DictVectorizer()
#     X = vectorizer.fit_transform(word_count_data)
#     y = [metadata['year'] for metadata in metadata_list]
#     return X, y, vectorizer

# # Main function for training with SVM
# def main(bag_of_words_folder):
#     print("Loading data...")
#     word_count_data, metadata_list = load_word_counts_and_metadata(bag_of_words_folder)

#     if not word_count_data or not metadata_list:
#         print("No valid data found for prediction.")
#         return
    
#     print("Preparing data for SVM model...")
#     X, y, vectorizer = prepare_data(word_count_data, metadata_list)
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     # Pipeline for SVM with optimized parameters using GridSearchCV
#     pipeline = Pipeline([
#         ('svm', SVR(kernel='rbf'))
#     ])

#     param_grid = {
#         'svm__C': [1, 10, 100],
#         'svm__gamma': ['scale', 0.01, 0.001]
#     }

#     grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
#     grid_search.fit(X_train, y_train)

#     print("Best parameters found:", grid_search.best_params_)
#     best_model = grid_search.best_estimator_

#     # Predict and evaluate
#     y_pred = best_model.predict(X_test)
#     mse = mean_squared_error(y_test, y_pred)
#     r2 = r2_score(y_test, y_pred)
    
#     print(f"Mean Squared Error: {mse}")
#     print(f"R-squared Score: {r2}")
    
#     # Show example predictions
#     print("\nExample Predictions (True Date vs Predicted Date):")
#     for true, pred in zip(y_test[:10], y_pred[:10]):
#         print(f"True Date: {true}, Predicted Date: {int(pred)}")

# # Specify the correct folder path
# bag_of_words_folder = 'data/counts'
# main(bag_of_words_folder)