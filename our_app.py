from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from collections import Counter
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import pickle
import random
import os
import re
import csv

app = Flask(__name__)
CORS(app)

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

# fail safe for reading files with different encodings
def get_file_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            text = file.read()
    except Exception as e:
        print(f"Error reading file: {file_path}")
        print(e)
        return None

    return text


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
    reader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
    first = True
    file_names = []
    actuals = []
    predictions = []
    titles = []
    authors = []
    
    for parts in reader:
        # skip first line
        if first:
            first = False
            continue

        file_names.append(parts[0])
        actuals.append(int(parts[1]))
        predictions.append(float(parts[2]))
        titles.append(parts[3])
        authors.append(parts[4])


############

TEXT_START_MARKERS = frozenset((
    "*END*THE SMALL PRINT",
    "*** START OF THE PROJECT GUTENBERG",
    "*** START OF THIS PROJECT GUTENBERG",
    "This etext was prepared by",
    "E-text prepared by",
    "Produced by",
    "Distributed Proofreading Team",
    "Proofreading Team at http://www.pgdp.net",
    "http://gallica.bnf.fr)",
    "      http://archive.org/details/",
    "http://www.pgdp.net",
    "by The Internet Archive)",
    "by The Internet Archive/Canadian Libraries",
    "by The Internet Archive/American Libraries",
    "public domain material from the Internet Archive",
    "Internet Archive)",
    "Internet Archive/Canadian Libraries",
    "Internet Archive/American Libraries",
    "material from the Google Print project",
    "*END THE SMALL PRINT",
    "***START OF THE PROJECT GUTENBERG",
    "This etext was produced by",
    "*** START OF THE COPYRIGHTED",
    "The Project Gutenberg",
    "http://gutenberg.spiegel.de/ erreichbar.",
    "Project Runeberg publishes",
    "Beginning of this Project Gutenberg",
    "Project Gutenberg Online Distributed",
    "Gutenberg Online Distributed",
    "the Project Gutenberg Online Distributed",
    "Project Gutenberg TEI",
    "This eBook was prepared by",
    "http://gutenberg2000.de erreichbar.",
    "This Etext was prepared by",
    "This Project Gutenberg Etext was prepared by",
    "Gutenberg Distributed Proofreaders",
    "Project Gutenberg Distributed Proofreaders",
    "the Project Gutenberg Online Distributed Proofreading Team",
    "**The Project Gutenberg",
    "*SMALL PRINT!",
    "More information about this book is at the top of this file.",
    "tells you about restrictions in how the file may be used.",
    "l'authorization à les utilizer pour preparer ce texte.",
    "of the etext through OCR.",
    "*****These eBooks Were Prepared By Thousands of Volunteers!*****",
    "We need your donations more than ever!",
    " *** START OF THIS PROJECT GUTENBERG",
    "****     SMALL PRINT!",
    '["Small Print" V.',
    '      (http://www.ibiblio.org/gutenberg/',
    'and the Project Gutenberg Online Distributed Proofreading Team',
    'Mary Meehan, and the Project Gutenberg Online Distributed Proofreading',
    '                this Project Gutenberg edition.',
))


TEXT_END_MARKERS = frozenset((
    "*** END OF THE PROJECT GUTENBERG",
    "*** END OF THIS PROJECT GUTENBERG",
    "***END OF THE PROJECT GUTENBERG",
    "End of the Project Gutenberg",
    "End of The Project Gutenberg",
    "Ende dieses Project Gutenberg",
    "by Project Gutenberg",
    "End of Project Gutenberg",
    "End of this Project Gutenberg",
    "Ende dieses Projekt Gutenberg",
    "        ***END OF THE PROJECT GUTENBERG",
    "*** END OF THE COPYRIGHTED",
    "End of this is COPYRIGHTED",
    "Ende dieses Etextes ",
    "Ende dieses Project Gutenber",
    "Ende diese Project Gutenberg",
    "**This is a COPYRIGHTED Project Gutenberg Etext, Details Above**",
    "Fin de Project Gutenberg",
    "The Project Gutenberg Etext of ",
    "Ce document fut presente en lecture",
    "Ce document fut présenté en lecture",
    "More information about this book is at the top of this file.",
    "We need your donations more than ever!",
    "END OF PROJECT GUTENBERG",
    " End of the Project Gutenberg",
    " *** END OF THIS PROJECT GUTENBERG",
))


LEGALESE_START_MARKERS = frozenset(("<<THIS ELECTRONIC VERSION OF",))
LEGALESE_END_MARKERS = frozenset(("SERVICE THAT CHARGES FOR DOWNLOAD",))


def strip_headers(text):
    """
    Remove lines that are part of the Project Gutenberg header or footer.

    Note: this function is a port of the C++ utility by Johannes Krugel. The
    original version of the code can be found at:
    http://www14.in.tum.de/spp1307/src/strip_headers.cpp

    Args:
        text (unicode): The body of the text to clean up.

    Returns:
        unicode: The text with any non-text content removed.

    """
    lines = text.splitlines()
    sep = str(os.linesep)

    out = []
    i = 0
    footer_found = False
    ignore_section = False

    for line in lines:
        reset = False

        if i <= 600:
            # Check if the header ends here
            if any(line.startswith(token) for token in TEXT_START_MARKERS):
                reset = True

            # If it's the end of the header, delete the output produced so far.
            # May be done several times, if multiple lines occur indicating the
            # end of the header
            if reset:
                out = []
                continue

        if i >= 100:
            # Check if the footer begins here
            if any(line.startswith(token) for token in TEXT_END_MARKERS):
                footer_found = True

            # If it's the beginning of the footer, stop output
            if footer_found:
                break

        if any(line.startswith(token) for token in LEGALESE_START_MARKERS):
            ignore_section = True
            continue
        elif any(line.startswith(token) for token in LEGALESE_END_MARKERS):
            ignore_section = False
            continue

        if not ignore_section:
            out.append(line.rstrip(sep))
            i += 1

    return sep.join(out)


file_skip_list = ['61063-0.txt']
chapter_list = ['Chapter', 'CHAPTER']

def chapter_in(sentence):
    for chapter in chapter_list:
        if chapter in sentence:
            return True
    return False


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
    
    text = data['text']
    print(text)
    processed_words = preprocess_text(text)
    word_counts = count_words(processed_words)
    prediction = svm_predict(word_counts)

    print(prediction)

    return jsonify({'prediction': prediction}), 200


# curl -X GET http://127.0.0.1:5000/random_sentence
@app.route('/random_sentence', methods=['GET'])
def random_sentence():
    for _ in range(10):
        index = random.randint(0, len(file_names) - 1)
        file = file_names[index]

        if file in file_skip_list:
            continue

        actual = actuals[index]
        prediction = predictions[index]
        title = titles[index]
        author = authors[index]

        text = get_file_text(f'data/raw/{file}')

        if text is None:
            continue

        clean_text = strip_headers(text).strip()
        sentences = re.split(r'[.!?]', clean_text)
        cleaned_sentences = [sentence.strip() for sentence in sentences[20:len(sentences) - 20] if len(sentence.strip()) > 100 and len(sentence.strip()) < 500 and not chapter_in(sentence)]

        if len(cleaned_sentences) == 0:
            continue

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
    
    return jsonify({'error': 'no random sentence found'}), 400


if __name__ == '__main__':
    app.run(debug=True)
