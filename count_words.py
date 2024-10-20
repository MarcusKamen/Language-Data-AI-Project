# import os
# import json
# from collections import Counter

# # Function to read files from the input folder
# def read_files(input_folder):
#     file_data = []
#     for filename in os.listdir(input_folder):
#         if filename.endswith(".txt"):
#             file_path = os.path.join(input_folder, filename)
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 file_data.append({
#                     "filename": filename,
#                     "content": f.read()
#                 })
#     return file_data

# # Function to count words in a file's content
# def count_words(content):
#     words = content.split()  # Simple split on spaces, consider better tokenization for more complex cases
#     word_counts = Counter(words)
#     return word_counts

# # Function to save the word count and metadata to a file
# def save_word_counts(word_counts, metadata, output_folder):
#     os.makedirs(output_folder, exist_ok=True)
#     output_file = os.path.join(output_folder, f"{metadata['filename']}_counts.json")
    
#     # Save both metadata and word count to a JSON file
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump({
#             "metadata": metadata,
#             "word_counts": dict(word_counts)
#         }, f, ensure_ascii=False, indent=4)

# def main(input_folder, output_folder):
#     files = read_files(input_folder)
    
#     for file_data in files:
#         word_counts = count_words(file_data['content'])
#         metadata = {
#             "filename": file_data["filename"],
#             "word_count": sum(word_counts.values())  # Total number of words
#         }
#         save_word_counts(word_counts, metadata, output_folder)
    
#     print(f"Word counts saved in folder: {output_folder}")

# if __name__ == "__main__":
#     # Set input folder and output folder paths
#     input_folder = "data/raw_clean"  # folder containing input text files
#     output_folder = "data/counts"  # folder to save word count files

#     main(input_folder, output_folder)

import os
import json
import re
from collections import Counter
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
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

# Function to read files from the input folder
def read_files(input_folder):
    file_data = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data.append({
                    "filename": filename,
                    "content": f.read()
                })
    return file_data

# Function to count words in the processed content
def count_words(processed_words):
    word_counts = Counter(processed_words)
    return word_counts

# Function to save the word count and metadata to a file
def save_word_counts(word_counts, metadata, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{metadata['filename']}_counts.json")
    
    # Save both metadata and word count to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "metadata": metadata,
            "word_counts": dict(word_counts)
        }, f, ensure_ascii=False, indent=4)

def main(input_folder, output_folder):
    files = read_files(input_folder)
    
    for file_data in files:
        # Preprocess content (remove punctuation, lemmatize, and stem)
        processed_words = preprocess_text(file_data['content'])
        
        # Count words
        word_counts = count_words(processed_words)
        
        metadata = {
            "filename": file_data["filename"],
            "word_count": sum(word_counts.values())  # Total number of words
        }
        
        # Save word counts with metadata
        save_word_counts(word_counts, metadata, output_folder)
    
    print(f"Word counts saved in folder: {output_folder}")

if __name__ == "__main__":
    # Set input folder and output folder paths
    input_folder = "data/raw_clean"  # folder containing input text files
    output_folder = "data/counts"    # folder to save word count files

    main(input_folder, output_folder)