import requests
from requests.exceptions import Timeout, RequestException
import os
from dotenv import load_dotenv

def main():
    title = input("Input the title: ").strip()

    author = input("Input the author: ").strip()
    returned = find_book(title, author)
    print(returned)


def find_book(title, author):
    ret = {'year': 10000, 'place': [], 'first_sentence': []}
    ret_open_library = find_book_open_library(title, author)
    ret_google_api = find_book_google_api(title, author)

    if 'error' in ret_open_library and 'error' in ret_google_api:
        return {'error': 'Both APIs failed', 'error_type': 'two'}
    if 'error' in ret_google_api:
        ret['year'] = int(ret_open_library['year'])
        ret['place'] = ret_open_library['place']
        ret['first_sentence'] = ret_open_library['first_sentence']
        ret['error'] = ret_google_api['error']
        ret['error_type'] = ret_google_api['error_type']
        return ret
    if 'error' in ret_open_library:
        ret['year'] = int(ret_google_api['year'])
        ret['place'] = ret_google_api['place']
        ret['first_sentence'] = ret_google_api['first_sentence']
        ret['error'] = ret_open_library['error']
        ret['error_type'] = ret_open_library['error_type']
        return ret

    if int(ret_open_library['year']) < int(ret_google_api['year']):
        ret['year'] = int(ret_open_library['year'])
    else:
        ret['year'] = int(ret_google_api['year'])

    ret['place'] = ret_open_library['place']
    ret['first_sentence'] = ret_open_library['first_sentence']
    return ret


# metadata returns a dictionary with the metadata of the book
def find_book_open_library(title, author):
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

    if 'docs' not in data:
        return ret

    docs = data['docs']

    for doc in docs:
        try:
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


def find_book_google_api(title, author):
    ret = {'year': 10000, 'place': [], 'first_sentence': []}  # starting with a year of 10000 so that found books can be less
    combined_title = title.replace(" ", "+")
    combined_author = author.replace(" ", "+")
    
    load_dotenv()
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{combined_title}+inauthor:{combined_author}+before:1950&key={api_key}'
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
    
    if 'items' not in data:
        return ret
    
    items = data['items']

    for item in items:
        doc = item['volumeInfo']
        try:
            print("matching book found in API")
            date = int(doc['publishedDate'].split('-')[0])
            if date < int(ret['year']):
                try:
                    ret['year'] = date
                except:
                    print("No year data")
        except:
            print("Error getting book information, skipping book in the list")

    print(ret)
    return ret


if __name__ == "__main__":
    main()
