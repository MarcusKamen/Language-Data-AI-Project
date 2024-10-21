import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error

# Function to load the JSON files containing word counts and metadata
def load_bag_of_words_data(bag_of_words_folder):
    word_count_data = []
    metadata_list = []
    
    for filename in os.listdir(bag_of_words_folder):
        if filename.endswith("_counts.json"):
            file_path = os.path.join(bag_of_words_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Append word counts and metadata
                word_count_data.append(data['word_counts'])
                metadata_list.append(data['metadata'])
    
    return word_count_data, metadata_list

# Function to prepare the feature matrix and target variable (dates)
def prepare_data(word_count_data, metadata_list):
    # Filter out entries where 'Year' is missing
    filtered_word_count_data = []
    filtered_metadata_list = []

    for word_counts, metadata in zip(word_count_data, metadata_list):
        if 'year' in metadata and metadata['year'] != "":
            filtered_word_count_data.append(word_counts)
            filtered_metadata_list.append(metadata)

    # Convert the word counts to a matrix using DictVectorizer
    vectorizer = DictVectorizer(sparse=False)
    X = vectorizer.fit_transform(filtered_word_count_data)
    
    # Extract the target variable (years) from the filtered metadata
    y = [int(metadata['year']) for metadata in filtered_metadata_list]
    
    return X, y, vectorizer

# Function to perform Ridge regression and evaluate the model
def run_ridge_regression(X, y):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize the Ridge regression model
    ridge_model = Ridge(alpha=1.0)
    
    # Fit the model to the training data
    ridge_model.fit(X_train, y_train)
    
    # Predict the test set
    y_pred = ridge_model.predict(X_test)
    
    # Calculate the mean squared error to evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse}")
    
    # Return the model and predictions
    return ridge_model, y_pred

# Main function to run the script
def main(bag_of_words_folder):
    # Load the bag-of-words data and metadata
    word_count_data, metadata_list = load_bag_of_words_data(bag_of_words_folder)
    
    # Prepare the feature matrix and target variable (dates)
    X, y, vectorizer = prepare_data(word_count_data, metadata_list)
    
    # Run Ridge regression and evaluate the model
    ridge_model, y_pred = run_ridge_regression(X, y)
    
    # Print some example predictions
    print("\nExample Predictions (True Date vs Predicted Date):")
    for true, pred in zip(y[:5], y_pred[:5]):
        print(f"True Date: {true}, Predicted Date: {int(pred)}")

if __name__ == "__main__":
    # Set the folder path where the word count JSON files are stored
    bag_of_words_folder = "data/counts"
    
    main(bag_of_words_folder)