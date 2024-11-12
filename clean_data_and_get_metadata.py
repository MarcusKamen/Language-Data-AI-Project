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


def print_cleaned_text(filename, text):
    clean_folder_path = './data/raw_clean/'

    with(open(f"{clean_folder_path}{filename}", 'w', encoding='utf-8')) as clean_file:
        clean_file.write(text)


def data_and_metadata(file_name_input):
    folder_path = './data/raw'
    not_found_file_path = './metadata/booksnotfound.csv'
    metadata_file_path = './metadata/metadata.csv'
    no_first_sentence_file_path = './metadata/nofirstsentence.csv'
    wrong_stars_file_path = './metadata/wrongstars.csv'
    no_start_file_path = './metadata/nostartdata.csv'

    if file_name_input == "":
        with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
            metadata_file.write("FileName,Title,Author,Year,Place\n")

        with open(not_found_file_path, 'w', encoding='utf-8') as not_metadata_file:
            not_metadata_file.write("FileName,Title,Author\n")

        with open(no_first_sentence_file_path, 'w', encoding='utf-8') as no_first_sentence_file:
            no_first_sentence_file.write("FileName,Title,Author,Year,Place\n")
        
        with open(wrong_stars_file_path, 'w', encoding='utf-8') as wrong_stars_file:
            wrong_stars_file.write("FileName,Title,Author,Year,Place\n")

        with open(no_start_file_path, 'w', encoding='utf-8') as no_start_file:
            no_start_file.write("FileName,Title,Author,Translator,Language\n")

    found_file = False
    for filename in os.listdir(folder_path):
        # Check if the file name is the one we want to start at
        if filename != file_name_input and not found_file and file_name_input != "":
            continue

        found_file = True
        print()
        file_path = os.path.join(folder_path, filename)

        # Check if it's a file (and not a directory)
        if not os.path.isfile(file_path):
            print(f"Skipping directory: {filename}")
            print_cleaned_text(filename, "")
            with open(no_start_file_path, 'a', encoding='utf-8', newline='') as no_start_file:
                writer = csv.writer(no_start_file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([filename, "", "", "", ""])
            continue
        
        print(f"Processing file: {filename}")

        text = get_file_text(file_path)
        
        if text is None:
            print("Skipping file because of error reading file")
            print_cleaned_text(filename, "")
            with open(no_start_file_path, 'a', encoding='utf-8', newline='') as no_start_file:
                writer = csv.writer(no_start_file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([filename, "", "", "", ""])
            continue
            
        if "Title: " in text:
            title = text.split("Title: ")[1].split("\n")[0]
            print(f"Title: {title}")
        else:
            print("Skipping file because title not found")
            print_cleaned_text(filename, text)
            with open(no_start_file_path, 'a', encoding='utf-8', newline='') as no_start_file:
                writer = csv.writer(no_start_file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([filename, "", "", "", ""])
            continue

        if "Author: " in text:
            author = text.split("Author: ")[1].split("\n")[0]
            if "by " in author:
                author = author.split("by ")[1]
            if "(AKA" in author and ")" in author:
                first_i = author.find("(AKA")
                second_i = author.find(")", first_i)
                author = author[:first_i] + author[second_i + 1:]
            if author == "Anonymous" or author == "Various":
                print("Skipping file because author is Anonymous or Various")
                print_cleaned_text(filename, text)
                with open(no_start_file_path, 'a', encoding='utf-8', newline='') as no_start_file:
                    writer = csv.writer(no_start_file, quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([filename, title, author, "", ""])
                continue
            print(f"Author: {author}")
        else:
            print("Skipping file because author not found")
            print_cleaned_text(filename, text)
            with open(no_start_file_path, 'a', encoding='utf-8', newline='') as no_start_file:
                writer = csv.writer(no_start_file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([filename, title, "", "", ""])
            continue

        # skip if different language
        if "Translator: " in text:
            translator = text.split("Translator: ")[1].split("\n")[0]
            print("Skipping file because it's a translation")
            print_cleaned_text(filename, text)
            with open(no_start_file_path, 'a', encoding='utf-8', newline='') as no_start_file:
                writer = csv.writer(no_start_file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([filename, title, author, translator, ""])
            continue

        if "Language: " in text:
            language = text.split("Language: ")[1].split("\n")[0]
            if language != "English":
                print("Skipping file because it's not in English")
                print_cleaned_text(filename, text)
                with open(no_start_file_path, 'a', encoding='utf-8', newline='') as no_start_file:
                    writer = csv.writer(no_start_file, quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([filename, title, author, "", language])
                continue
            print(f"Language: {language}")


        metadata = get_metadata.find_book(title, author)

        if 'error' in metadata:
            print(f"Error: {metadata['error']}, {metadata['error_type']}")
            print('Some metadata sources failed')

        if ('year' in metadata and (int(metadata['year']) > 2000 or int(metadata['year']) < 1000)) or ('error' in metadata and not 'year' in metadata):
            print("No metadata found, writing to booksnotfound.csv")

            # Prepare the entry to write
            # entry = f"{title},{author}\n"

            # with open(not_found_file_path, 'a', encoding='utf-8', errors='replace') as not_metadata_file:
            #     existing_entries = not_metadata_file.readlines()
                    
            # Check if the entry already exists
            # if entry not in existing_entries:
            print_cleaned_text(filename, text)
            with open(not_found_file_path, 'a', encoding='utf-8', newline='') as not_metadata_file:
                writer = csv.writer(not_metadata_file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([filename, title, author])
                    # metadata_file.write(entry)s
            continue


        place = metadata['place']
        year = metadata['year']
        first_sentence = metadata['first_sentence']

        text = strip_headers(text)

        min_loc = -1
        # make only alphabetic characters for testing
        test_text = ''.join([char for char in text if char.isalpha()]).lower()

        for sentence in first_sentence:
            test_sentence = ''.join([char for char in sentence if char.isalpha()]).lower()
            if test_sentence in test_text:
                sentence_loc = test_text.find(test_sentence)
                if (min_loc == -1 or sentence_loc < min_loc):
                    min_loc = sentence_loc

        if min_loc == -1:
            print("No first sentence found, writing to no_first_sentence.csv")
            with open(no_first_sentence_file_path, 'a', encoding='utf-8', newline='') as no_first_sentence_file:
                writer = csv.writer(no_first_sentence_file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([filename, title, author, year, place])

            clean_text = text[:]
            
            while "Chapter 1".lower() in clean_text.lower() or "Chapter I".lower() in clean_text.lower():
                next_loc = -1
                if "Chapter 1".lower() in clean_text.lower():
                    next_loc = clean_text.lower().find("Chapter 1".lower())
                if "Chapter I".lower() in clean_text.lower():
                    next_loc_2 = clean_text.lower().find("Chapter I".lower())
                    if next_loc == -1 or next_loc_2 < next_loc:
                        next_loc = next_loc_2
                
                next_loc = next_loc + 9
                clean_text = clean_text[next_loc:]

            print_cleaned_text(filename, clean_text)
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

        clean_text = text[original_index:]
        print("Found all needed information, adding metadata and cleaned data")
        
        print_cleaned_text(filename, clean_text)
        
        with open(metadata_file_path, 'a', encoding='utf-8', newline='') as metadata_file:
            writer = csv.writer(metadata_file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow([filename, title, author, year, place])


def main():
    ans1 = input("Would you like to start at a specific file (y/n)? ").strip()
    if ans1.lower().strip() == "y":
        ans2 = input("What is the file name (Note: You will only write more to the metadata files rather than writing over)? ").strip()
    else:
        ans2 = ""
    data_and_metadata(ans2)


if __name__ == "__main__":
    main()
