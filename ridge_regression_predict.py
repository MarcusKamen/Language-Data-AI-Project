# import json
# import os
# import numpy as np
# from sklearn.linear_model import Ridge
# from sklearn.feature_extraction import DictVectorizer

# def load_word_counts_and_metadata(folder):
#     word_count_data = []
#     metadata_list = []
    
#     for filename in os.listdir(folder):
#         if filename.endswith("_counts.json"):
#             file_path = os.path.join(folder, filename)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     data = json.load(file)
                    
#                     # Extract year and word count
#                     year = data.get('metadata', {}).get('year')
#                     word_count = data.get('word_count')
                    
#                     # Skip invalid years and word counts
#                     if year and isinstance(year, int) and 1000 <= year <= 2000:
#                         word_count_data.append(data)  # Assuming data is a dictionary
#                         metadata_list.append(year)
#                     else:
#                         print(f"Skipped {filename}: Invalid year {year}")
#             except KeyError as e:
#                 print(f"Error reading {filename}: {e}")
#             except json.JSONDecodeError:
#                 print(f"Error decoding JSON from {filename}.")
    
#     return word_count_data, metadata_list

# def prepare_data(word_count_data, metadata_list):
#     vectorizer = DictVectorizer()
    
#     # Create features (X) and labels (y)
#     X = vectorizer.fit_transform(word_count_data)
#     y = np.array(metadata_list)
    
#     return X, y, vectorizer

# def main(bag_of_words_folder):
#     print("Loading data...")
#     word_count_data, metadata_list = load_word_counts_and_metadata(bag_of_words_folder)
    
#     if not word_count_data or not metadata_list:
#         print("No valid data found for prediction.")
#         return
    
#     X, y, vectorizer = prepare_data(word_count_data, metadata_list)
    
#     # Train the model
#     model = Ridge()
#     model.fit(X, y)

#     # Make predictions
#     predictions = model.predict(X)
    
#     # Print expected vs predicted
#     print("\nExpected year vs Predicted year:")
#     for expected, predicted in zip(y, predictions):
#         print(f"Expected: {expected} - Predicted: {predicted:.2f}")

# if __name__ == "__main__":
#     bag_of_words_folder = 'data/counts'  # Adjust this path as necessary
#     main(bag_of_words_folder)






import os
import json
from sklearn.linear_model import Ridge
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
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

# Specify the correct folder path
bag_of_words_folder = 'data/counts'  # Adjust if needed
main(bag_of_words_folder)




# import os
# import json
# import numpy as np
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import Ridge
# from sklearn.feature_extraction import DictVectorizer
# from sklearn.metrics import mean_squared_error
# import os
# import json
# from sklearn.feature_extraction import DictVectorizer
# from sklearn.linear_model import Ridge

# # # Function to load the JSON files containing word counts and metadata
# # def load_bag_of_words_data(bag_of_words_folder):
# #     word_count_data = []
# #     metadata_list = []
    
# #     for filename in os.listdir(bag_of_words_folder):
# #         if filename.endswith("_counts.json"):
# #             file_path = os.path.join(bag_of_words_folder, filename)
# #             with open(file_path, 'r', encoding='utf-8') as f:
# #                 data = json.load(f)
                
# #                 # Append word counts and metadata
# #                 word_count_data.append(data['word_counts'])
# #                 metadata_list.append(data['metadata'])
    
# #     return word_count_data, metadata_list
# def load_word_counts_and_metadata(folder):
#     word_count_data = []
#     metadata_list = []

#     for filename in os.listdir(folder):
#         if filename.endswith(".json"):
#             file_path = os.path.join(folder, filename)
#             with open(file_path, 'r') as file:
#                 data = json.load(file)
#                 # Append the word count and metadata
#                 word_count_data.append(data.get('word_counts', {}))
#                 metadata_list.append(data.get('metadata', {}))
#                 print(f"Loaded data for file: {filename}")

#     return word_count_data, metadata_list

# # Function to prepare the feature matrix and target variable (dates)
# # def prepare_data(word_count_data, metadata_list):
# #     # Filter out entries where 'year' is missing
# #     filtered_word_count_data = []
# #     filtered_metadata_list = []

# #     for word_counts, metadata in zip(word_count_data, metadata_list):
# #         if 'year' in metadata and metadata['year'] != "":
# #             filtered_word_count_data.append(word_counts)
# #             filtered_metadata_list.append(metadata)

# #     # Convert the word counts to a matrix using DictVectorizer
# #     vectorizer = DictVectorizer(sparse=False)
# #     X = vectorizer.fit_transform(filtered_word_count_data)
    
# #     # Extract the target variable (years) from the filtered metadata
# #     y = [int(metadata['year']) for metadata in filtered_metadata_list]
    
# #     return X, y, vectorizer

# # Function to perform Ridge regression and evaluate the model
# def run_ridge_regression(X, y):
#     # Split the data into training and testing sets
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
#     # Initialize the Ridge regression model
#     ridge_model = Ridge(alpha=1.0)
    
#     # Fit the model to the training data
#     ridge_model.fit(X_train, y_train)
    
#     # Predict the test set
#     y_pred = ridge_model.predict(X_test)
    
#     # Calculate the mean squared error to evaluate the model
#     mse = mean_squared_error(y_test, y_pred)
    
#     print(f"Mean Squared Error: {mse}")
    
#     # Return the model and predictions
#     return ridge_model, y_pred
# def prepare_data(word_count_data, metadata_list):
#     # Filter entries to only include those with 'year' between 1000 and 2000
#     filtered_word_count_data = []
#     filtered_metadata_list = []

#     for word_counts, metadata in zip(word_count_data, metadata_list):
#         # Check if 'year' exists and is within the range
#         if 'year' in metadata:
#             year = int(metadata['year'])
#             if 1000 <= year <= 2000:
#                 filtered_word_count_data.append(word_counts)
#                 filtered_metadata_list.append(metadata)
#                 print(f"Accepted file with year: {year}")
#             else:
#                 print(f"Ignored file with year: {year}")
#         else:
#             print("Ignored file with no year.")

#     # Ensure filtered data is not empty
#     if not filtered_word_count_data:
#         print("No data available within the 1000-2000 year range.")
#         return None, None, None

#     # Convert the word counts to a matrix using DictVectorizer
#     vectorizer = DictVectorizer(sparse=False)
#     X = vectorizer.fit_transform(filtered_word_count_data)
    
#     # Extract the target variable (years) from the filtered metadata
#     y = [int(metadata['year']) for metadata in filtered_metadata_list]
    
#     return X, y, vectorizer

# def main(bag_of_words_folder):
#     # Load the data
#     print("Loading data...")
#     word_count_data, metadata_list = load_word_counts_and_metadata(bag_of_words_folder)
#     print(f"Total files loaded: {len(word_count_data)}")

#     # Prepare the data
#     print("Preparing data...")
#     X, y, vectorizer = prepare_data(word_count_data, metadata_list)
    
#     if X is None or y is None:
#         print("Terminating due to lack of valid data.")
#         return

#     # Proceed with Ridge Regression if data is valid
#     ridge_model = Ridge(alpha=1.0)
#     ridge_model.fit(X, y)

#     # Example prediction
#     print("Model trained successfully.")

# if __name__ == "__main__":
#     bag_of_words_folder = 'data/processed_bag_of_words'
#     main(bag_of_words_folder)
# # def main(bag_of_words_folder):
# #     # Load the bag-of-words data and metadata
# #     word_count_data, metadata_list = load_bag_of_words_data(bag_of_words_folder)
    
# #     # Prepare the feature matrix and target variable (dates)
# #     X, y, vectorizer = prepare_data(word_count_data, metadata_list)
    
# #     # Run Ridge regression and evaluate the model
# #     ridge_model, y_pred = run_ridge_regression(X, y)
    
# #     # Print some example predictions
# #     print("\nExample Predictions (True Date vs Predicted Date):")
# #     for true, pred in zip(y[:5], y_pred[:5]):
# #         print(f"True Date: {true}, Predicted Date: {int(pred)}")

# # if __name__ == "__main__":
# #     # Set the folder path where the word count JSON files are stored
# #     bag_of_words_folder = "data/counts"
    
# #     main(bag_of_words_folder)