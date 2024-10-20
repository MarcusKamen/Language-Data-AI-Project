import requests
from requests.exceptions import Timeout, RequestException

# for each book

# Create a call that will

def main():
    title = input("Input the title: ").strip()

    author = input("Input the author: ").strip()
    returned = find_book(title, author)
    print(returned)


# metadata returns a dictionary with the metadata of the book
def find_book(title, author):
    ret = {'year': 10000, 'place': [], 'first_sentence': []}  # starting with a year of 10000 so that found books can be less
    combined = (title.replace(" ", "+") + "+" + author.replace(" ", "+"))

    url = "https://openlibrary.org/search.json?q=" + combined
    print(url)

    try:
        # Set a timeout value in seconds
        response = requests.get(url, timeout=10)
        
        # Check if the response was successful (status code 200)
        response.raise_for_status()
        data = response.json()
    except Timeout as e:
        return {'error': str(e), 'error_type': 'Timeout'}
    except RequestException as e:
        return {'error': str(e), 'error_type': 'RequestException'}


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
                    ret['place'] += doc['place'] 
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
# Account for weird author attributions in pg