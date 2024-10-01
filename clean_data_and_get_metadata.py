import os
import get_metadata
import csv

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


def main():
    folder_path = './data/raw'
    clean_folder_path = './data/raw_clean/'
    not_found_file_path = './metadata/booksnotfound.csv'
    metadata_file_path = './metadata/metadata.csv'

    with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
        metadata_file.write("FileName,Title,Author,Year,Place\n")

    with open(not_found_file_path, 'w', encoding='utf-8') as not_metadata_file:
        not_metadata_file.write("FileName,Title,Author\n")

    # set break condition to for loop for testing purposes
    i = 0

    for filename in os.listdir(folder_path):
        print()

        if i == 100:
            break

        i += 1
        file_path = os.path.join(folder_path, filename)

        # Check if it's a file (and not a directory)
        if not os.path.isfile(file_path):
            print(f"Skipping directory: {filename}")
            continue
        
        print(f"Processing file: {filename}")

        text = get_file_text(file_path)
        
        if text is None:
            continue
            
        if "Title: " in text:
            title = text.split("Title: ")[1].split("\n")[0]
            print(f"Title: {title}")
        else:
            print("Skipping file because title not found")
            continue

        if "Author: " in text:
            author = text.split("Author: ")[1].split("\n")[0]
            if author == "Anonymous" or author == "Various":
                print("Skipping file because author is Anonymous or Various")
                continue
            print(f"Author: {author}")
        else:
            print("Skipping file because author not found")
            continue

        # skip if different language
        if "Translator: " in text:
            print("Skipping file because it's a translation")
            continue

        if "Language: " in text:
            language = text.split("Language: ")[1].split("\n")[0]
            if language != "English":
                print("Skipping file because it's not in English")
                continue
            print(f"Language: {language}")


        metadata = get_metadata.find_book(title, author)

        if metadata == {'year': 10000, 'place': [], 'first_sentence': []}:
            print("Book not found!")

            # Prepare the entry to write
            entry = f"{title},{author}\n"

            with open(not_found_file_path, 'r', encoding='utf-8', errors='replace') as not_metadata_file:
                existing_entries = not_metadata_file.readlines()
                    
            # Check if the entry already exists
            if entry not in existing_entries:
                with open(not_found_file_path, 'a', encoding='utf-8', newline='') as not_metadata_file:
                    writer = csv.writer(not_metadata_file, quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([filename, title, author])
                    # metadata_file.write(entry)s
            continue


        place = metadata['place']
        year = metadata['year']
        first_sentence = metadata['first_sentence']

        # Assuming first_sentence is a list of possible first_sentences
        if "***" in text:
            first_star_loc = text.find("***")
            try:
                second_star_loc = text.find("***", first_star_loc + 1)
                third_star_loc = text.find("***", second_star_loc + 1)
            except:
                print("Skipping file because not enough *** found")
                continue
        else:
            print("Skipping file because *** not found")
            continue

        min_loc = -1
        # make only alphabetic characters for testing
        test_text = ''.join([char for char in text if char.isalpha()]).lower()

        for sentence in first_sentence:
            test_sentence = ''.join([char for char in sentence if char.isalpha()]).lower()
            if test_sentence in test_text:
                sentence_loc = test_text.find(test_sentence)
                if sentence_loc > second_star_loc and (min_loc == -1 or sentence_loc < min_loc):
                    min_loc = sentence_loc

        if min_loc == -1:
            print("Skipping file because first sentence not found")
            continue

        # map to original index
        count = 0
        original_index = -1
        for index, char in enumerate(text.lower()):
            if not char.isalpha(): # match white space or dash
                count += 1
            if index - count == min_loc:
                original_index = index
                break

        clean_text = text[original_index:third_star_loc]
        print("Found all needed information, adding metadata and cleaned data")
        
        with(open(f"{clean_folder_path}{filename}", 'w', encoding='utf-8')) as clean_file:
            clean_file.write(clean_text)
        
        with open(metadata_file_path, 'a', encoding='utf-8', newline='') as metadata_file:
            writer = csv.writer(metadata_file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([filename, title, author, year, place])


if __name__ == "__main__":
    main()
