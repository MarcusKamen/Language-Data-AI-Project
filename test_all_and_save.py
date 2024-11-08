import pickle
import os
import json
import tensorflow as tf
import csv

COUNTS_DATA_PATH = 'data/counts/'
CLEANED_DATA_PATH = 'data/raw_clean/'

SVM_MODEL_PATH = "models/svm/svm_model.pkl"
SVM_VECTORIZER_PATH = "models/svm/vectorizer.pkl"
SVM_PRED_SAVE_PATH = "models/svm/all_results.csv"

RIDGE_MODEL_PATH = "models/ridge/ridge_model.pkl"
RIDGE_VECTORIZER_PATH = "models/ridge/vectorizer.pkl"
RIDGE_PRED_SAVE_PATH = "models/ridge/all_results.csv"

NEURAL_MODEL_PATH = "models/neural/text_year_model.h5"
NEURAL_VECTORIZER_PATH = "models/neural/tfidf_vectorizer.pkl"
NEURAL_SCALER_PATH = "models/neural/scaler.pkl"
NEURAL_PRED_SAVE_PATH = "models/neural/all_results.csv"

def svm_predict_all():
    with open(SVM_MODEL_PATH, 'rb') as file:
        svm_model = pickle.load(file)
    with open(SVM_VECTORIZER_PATH, 'rb') as file:
        vectorizer = pickle.load(file)

    actuals = []
    predictions = []
    file_list = []
    titles = []
    authors = []

    for file in os.listdir(COUNTS_DATA_PATH):
        if not file.endswith('_counts.json'):
            continue

        with open(os.path.join(COUNTS_DATA_PATH, file), 'r', encoding='utf-8') as f:
            test_info = json.load(f)
            if not 'metadata' in test_info:
                continue
            metadata = test_info['metadata']

            if not 'year' in metadata or metadata['year'] == "" or int(metadata['year']) < 1000 or int(metadata['year']) > 2000:
                continue
            year = int(metadata['year'])

            if not 'word_counts' in test_info:
                continue
            counts = test_info['word_counts']

            if not 'filename' in metadata:
                continue
            filename = metadata['filename']

            if not 'title' in metadata:
                continue
            title = metadata['title']

            if not 'author' in metadata:
                continue
            author = metadata['author']

            vectorized_counts = vectorizer.transform([counts])
            pred = svm_model.predict(vectorized_counts)

            actuals.append(year)
            predictions.append(pred[0])
            file_list.append(filename)
            titles.append(title)
            authors.append(author)

    return file_list, actuals, predictions, titles, authors


def ridge_predict_all(counts):
    with open(RIDGE_MODEL_PATH, 'rb') as file:
        ridge_model = pickle.load(file)
    with open(RIDGE_VECTORIZER_PATH, 'rb') as file:
        vectorizer = pickle.load(file)
    
    actuals = []
    predictions = []
    file_list = []
    titles = []
    authors = []

    for file in os.listdir(COUNTS_DATA_PATH):
        if not file.endswith('_counts.json'):
            continue

        with open(os.path.join(COUNTS_DATA_PATH, file), 'r', encoding='utf-8') as f:
            test_info = json.load(f)
            if not 'metadata' in test_info:
                continue
            metadata = test_info['metadata']

            if not 'year' in metadata or metadata['year'] == "" or int(metadata['year']) < 1000 or int(metadata['year']) > 2000:
                continue
            year = int(metadata['year'])

            if not 'word_counts' in test_info:
                continue
            counts = test_info['word_counts']

            if not 'filename' in metadata:
                continue
            filename = metadata['filename']

            if not 'title' in metadata:
                continue
            title = metadata['title']

            if not 'author' in metadata:
                continue
            author = metadata['author']

            vectorized_counts = vectorizer.transform([counts])
            pred = ridge_model.predict(vectorized_counts)

            actuals.append(year)
            predictions.append(pred[0])
            file_list.append(filename)
            titles.append(title)
            authors.append(author)

    return file_list, actuals, predictions, titles, authors


def neural_predict_all(test_data):
    with open(NEURAL_VECTORIZER_PATH, 'rb') as file:
        vectorizer = pickle.load(file)
    model = tf.keras.models.load_model(NEURAL_MODEL_PATH)
    with open(NEURAL_SCALER_PATH, 'rb') as file:
        scaler = pickle.load(file)

    actuals = []
    predictions = []
    file_list = []
    titles = []
    authors = []

    for file in os.listdir(COUNTS_DATA_PATH):
        if file.endswith('_counts.json'):
            continue

        with open(os.path.join(COUNTS_DATA_PATH, file), 'r', encoding='utf-8') as f:
            test_info = json.load(f)
            if not 'metadata' in test_info:
                continue
            metadata = test_info['metadata']

            if not 'year' in metadata or metadata['year'] == "" or int(metadata['year']) < 1000 or int(metadata['year']) > 2000:
                continue
            year = int(metadata['year'])

            if not 'filename' in metadata:
                continue
            filename = metadata['filename']

            if not 'title' in metadata:
                continue
            title = metadata['title']

            if not 'author' in metadata:
                continue
            author = metadata['author']

            with open(os.path.join(CLEANED_DATA_PATH, filename), 'r', encoding='utf-8') as g:
                test_data = g.read()

            vectorized_data = vectorizer.transform([test_data])
            scaled_data = scaler.transform(vectorized_data.toarray())
            pred = model.predict(scaled_data)

            actuals.append(year)
            predictions.append(pred[0][0])
            file_list.append(filename)
            titles.append(title)
            authors.append(author)

    return file_list, actuals, predictions, titles, authors


def main(model_name):
    if model_name == 'svm':
        save_path = SVM_PRED_SAVE_PATH
        file_list, actuals, predictions, titles, authors = svm_predict_all()
    elif model_name == 'ridge':
        save_path = RIDGE_PRED_SAVE_PATH
        file_list, actuals, predictions, titles, authors = ridge_predict_all()
    elif model_name == 'neural':
        save_path = NEURAL_PRED_SAVE_PATH
        file_list, actuals, predictions, titles, authors = neural_predict_all()
    else:
        print("Invalid model name")
        return
    
    with open(save_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Filename", "Actual", "Predicted", "Title", "Author"])
        for file, actual, pred, title, author in zip(file_list, actuals, predictions, titles, authors):
            writer.writerow([file, actual, pred, title, author])


if __name__ == '__main__':
    model_name = input("Input the model you would like to use and save all results (svm / ridge / neural): ").strip()
    main(model_name)