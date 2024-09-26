import os

folder_path = './data/raw'

# set break condition to for loop for testing purposes
i = 0

for filename in os.listdir(folder_path):
    i += 1
    file_path = os.path.join(folder_path, filename)

    # Check if it's a file (and not a directory)
    if not os.path.isfile(file_path):
        print(f"Skipping directory: {filename}")
        continue
    
    print(f"Processing file: {filename}")

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        
        if "Title: " in text:
            title = text.split("Title: ")[1].split("\n")[0]
            print(f"Title: {title}")
        else:
            title = "Title not found"
            print(f"Title: {title}")

        if "Author: " in text:
            author = text.split("Author: ")[1].split("\n")[0]
            print(f"Author: {author}")
        else:
            author = "Author not found"
            print(f"Author: {author}")

        # skip if different language
        if "Translator: " in text:
            continue

    print()

    if i == 10:
        break
