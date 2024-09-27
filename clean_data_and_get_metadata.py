import os

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

    # set break condition to for loop for testing purposes
    i = 0

    for filename in os.listdir(folder_path):
        print()

        if i == 10:
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

        # TODO
        # Call API to get metadata using author and title information
        first_sentence = []

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
        for sentence in first_sentence:
            if sentence in text:
                sentence_loc = text.find(sentence)
                if sentence_loc > second_star_loc and (min_loc == -1 or sentence_loc < min_loc):
                    min_loc = sentence_loc

        if min_loc == -1:
            print("Skipping file because first sentence not found")
            continue

        clean_text = text[min_loc:third_star_loc]
        print("Found all needed information, adding metadata and cleaned data")
        
        with(open(f"./data/raw_cleaned/{filename}", 'w', encoding='utf-8')) as clean_file:
            clean_file.write(clean_text)

        # TODO
        # add metadata to csv file


if __name__ == "__main__":
    main()
