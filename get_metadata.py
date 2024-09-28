import requests

# for each book

# Create a call that will

def main():
    title = input("Input the title: ").strip()

    author = input("Input the author: ").strip()
    returned = find_book(title, author)
    print(returned)


# metadata returns a dictionary with the metadata of the book
def find_book(title, author):
    ret = {'year': 10000, 'place': "", 'first_sentence': []}  # starting with a year of 10000 so that found books can be less
    combined = (title.replace(" ", "+") + "+" + author.replace(" ", "+"))

    url = "https://openlibrary.org/search.json?q=" + combined
    print(url)
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response as JSON
        data = response.json()
        
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


    docs = data['docs']

    for doc in docs:
        try:
            # FIXME, authors can cause misattributions. ex:Uncle Silas by J. S. LeFanu
            if doc['title'].lower() == title.lower() and doc['author_name'][0].lower() == author.lower():
                print("matching book found in API")
                
                if (doc['first_publish_year'] < ret['year']):
                    try:
                        ret['year'] = doc['first_publish_year']
                    except:
                        print("No year data")
                try:
                    ret['place'] = doc['place'] + " " + ret['place']
                except:
                    print("No place data")
                try:
                    for sentence in doc['first_sentence']:
                        ret['first_sentence'].append(sentence)
                except:
                    print('No first sentence')

        except:
            print("Error getting book information, skipping book in the list")

    return ret


if __name__ == "__main__":
    main()
# TODO:
# Put data into csv file
# Account for weird author attributions in pg