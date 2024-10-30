import pickle
import os
import json
import tensorflow as tf

COUNTS_DATA_PATH = 'data/counts/'
CLEANED_DATA_PATH = 'data/raw_clean/'

SVM_MODEL_PATH = "models/svm/svm_model.pkl"
SVM_VECTORIZER_PATH = "models/svm/vectorizer.pkl"
RIDGE_MODEL_PATH = "models/ridge/ridge_model.pkl"
RIDGE_VECTORIZER_PATH = "models/ridge/vectorizer.pkl"
NEURAL_MODEL_PATH = "models/neural/text_year_model.h5"
NEURAL_VECTORIZER_PATH = "models/neural/tfidf_vectorizer.pkl"
NEURAL_SCALER_PATH = "models/neural/scaler.pkl"

def svm_predict(counts):
    with open(SVM_MODEL_PATH, 'rb') as file:
        svm_model = pickle.load(file)
    with open(SVM_VECTORIZER_PATH, 'rb') as file:
        vectorizer = pickle.load(file)

    vectorized_counts = vectorizer.transform([counts])
    prediction = svm_model.predict(vectorized_counts)
    return prediction[0]


def ridge_predict(counts):
    with open(RIDGE_MODEL_PATH, 'rb') as file:
        ridge_model = pickle.load(file)
    with open(RIDGE_VECTORIZER_PATH, 'rb') as file:
        vectorizer = pickle.load(file)
    
    vectorized_counts = vectorizer.transform([counts])
    prediction = ridge_model.predict(vectorized_counts)
    return prediction[0]


def neural_predict(test_data):
    with open(NEURAL_VECTORIZER_PATH, 'rb') as file:
        vectorizer = pickle.load(file)
    model = tf.keras.models.load_model(NEURAL_MODEL_PATH)
    with open(NEURAL_SCALER_PATH, 'rb') as file:
        scaler = pickle.load(file)

    vectorized_data = vectorizer.transform([test_data])
    scaled_data = scaler.transform(vectorized_data.toarray())
    prediction = model.predict(scaled_data)
    return prediction[0][0]


def main(model_name, test_file):
    test_data_path = os.path.join(CLEANED_DATA_PATH, test_file)
    counts_file = test_file + "_counts.json"
    test_counts_path = os.path.join(COUNTS_DATA_PATH, counts_file)

    with open(test_data_path, 'r', encoding='utf-8') as file:
        test_data = file.read()

    with open(test_counts_path, 'r', encoding='utf-8') as file:
        test_counts = json.load(file)

    metadata = test_counts.get('metadata', {})
    counts = test_counts.get('word_counts', {})
    if not 'year' in metadata or metadata['year'] == "" or int(metadata['year']) < 1000 or int(metadata['year']) > 2000:
        print("No valid year data found in test file")
        return
    
    actual = int(metadata['year'])
    title = metadata['title']
    author = metadata['author']
    
    if title == "":
        title = "(Unknown Title)"
    if author == "":
        author = "(Unknown Author)"

    if model_name == 'svm':
        prediction = svm_predict(counts)
    elif model_name == 'ridge':
        prediction = ridge_predict(counts)
    elif model_name == 'neural':
        prediction = neural_predict(test_data)
    else:
        print("Invalid model name")
        return

    print(f'Comparison of Prediction and Actual for {title} by {author} with {model_name} model:')
    print(f'Actual: {actual}')
    print(f'Prediction: {prediction}')


if __name__ == '__main__':
    model_name = input("Input the model you would like to use (svm / ridge / neural): ").strip()
    test_file = input("Input the file you would like to test: ").strip()
    main(model_name, test_file)