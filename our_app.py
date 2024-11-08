from flask import Flask, jsonify, request
import re
from collections import Counter
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import pickle
import random

app = Flask(__name__)

nltk.download('punkt')
nltk.download('punkt_tab')

# Download necessary NLTK data if not already present
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize lemmatizer and stemmer
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# Function to remove punctuation and tokenize
def preprocess_text(content):
    # Remove punctuation using regex
    content = re.sub(r'[^\w\s]', '', content)
    
    # Tokenize the content
    words = nltk.word_tokenize(content)
    
    # Lemmatize and stem words
    processed_words = [stemmer.stem(lemmatizer.lemmatize(word.lower())) for word in words]
    
    return processed_words

# Function to count words in the processed content
def count_words(processed_words):
    word_counts = Counter(processed_words)
    return dict(word_counts)


SVM_MODEL_PATH = "final_pickles/svm/svm_model.pkl"
SVM_VECTORIZER_PATH = "final_pickles/svm/vectorizer.pkl"
SVM_PRED_SAVE_PATH = "final_pickles/svm/all_results.csv"

with open(SVM_MODEL_PATH, 'rb') as file:
    svm_model = pickle.load(file)
with open(SVM_VECTORIZER_PATH, 'rb') as file:
    vectorizer = pickle.load(file)

def svm_predict(counts):
    vectorized_counts = vectorizer.transform([counts])
    prediction = svm_model.predict(vectorized_counts)
    return prediction[0]

with open(SVM_PRED_SAVE_PATH, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    first = True
    file_names = []
    actuals = []
    predictions = []
    titles = []
    authors = []
    
    for line in lines:
        # skip first line
        if first:
            first = False
            continue

        parts = line.strip().split(',')
        file_names.append(parts[0])
        actuals.append(int(parts[1]))
        predictions.append(float(parts[2]))
        titles.append(parts[3])
        authors.append(parts[4])


# curl -X GET http://127.0.0.1:5000/
@app.route('/', methods=['GET'])
def index():
    return jsonify({'data': 'Hello, World!'}), 200


# curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"text": "This is a sample text for prediction."}'
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if 'text' not in data:
        return jsonify({'error': 'no text provided'}), 400
    
    print('k')
    text = data['text']
    processed_words = preprocess_text(text)
    word_counts = count_words(processed_words)
    prediction = svm_predict(word_counts)

    return jsonify({'prediction': prediction}), 200


# curl -X GET http://127.0.0.1:5000/random_sentence
@app.route('/random_sentence', methods=['GET'])
def random_sentence():
    index = random.randint(0, len(file_names) - 1)
    file = file_names[index]
    actual = actuals[index]
    prediction = predictions[index]
    title = titles[index]
    author = authors[index]

    with open(f'data/raw/{file}', 'r', encoding='utf-8') as f:
        text = f.read()

    first_star_loc = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    second_star_loc = text.find("***", first_star_loc + 3)
    third_star_loc = text.find("*** END OF THE PROJECT GUTENBERG EBOOK", second_star_loc + 3)
    forth_star_loc = text.find("***", third_star_loc + 3)

    if forth_star_loc == -1:
        return jsonify({'error': 'no random sentence found'}), 400
    
    clean_text = text[second_star_loc:third_star_loc].strip()
    sentences = clean_text.split('.')
    cleaned_sentences = [sentence.strip() for sentence in sentences[20:len(sentences) - 20] if len(sentence.strip()) > 100]
    random_sentence = random.choice(cleaned_sentences)

    return jsonify(
        {
            'file_name': file,
            'actual': actual,
            'prediction': prediction,
            'random_sentence': random_sentence,
            'title': title,
            'author': author
        }), 200


if __name__ == '__main__':
    app.run(debug=True)
