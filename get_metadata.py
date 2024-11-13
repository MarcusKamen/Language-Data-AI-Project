import requests
from requests.exceptions import Timeout, RequestException
import os
from dotenv import load_dotenv
import scrape_google
import json

def main():
    title = input("Input the title: ").strip()
    author = input("Input the author: ").strip()
    print_results = input("Would you like to print the results of the metadata api queries in corresponding files? (y/n): ").strip()
    
    if print_results == 'y':
        print_results = True
        os.makedirs('metadata/single_results', exist_ok=True)
    else:
        print_results = False

    returned = find_book(title, author, print_results)
    print(returned)


def find_book(title, author, print_results=False):
    ret = {'year': 10000, 'place': [], 'first_sentence': []}
    ret_open_library = find_book_open_library(title, author, print_results)
    ret_scrape_google = get_scrape_google(title, author, print_results)

    if 'year' in ret_open_library:
        ret['year'] = min(ret['year'], ret_open_library['year'])
    if ret_scrape_google < ret['year']:
        ret['year'] = ret_scrape_google

    if (ret['year'] >= 1950 and ret['year'] < 2050) or print_results:
        ret_google_api = find_book_google_api(title, author, print_results)     
    else:
        ret_google_api = {'year': 10000, 'place': [], 'first_sentence': []}

    if 'year' in ret_google_api:
        ret['year'] = min(ret['year'], ret_google_api['year'])

    if 'place' in ret_open_library:
        ret['place'] = ret_open_library['place']
    if 'first_sentence' in ret_open_library:
        ret['first_sentence'] = ret_open_library['first_sentence']

    if 'error' in ret_open_library and 'error' in ret_google_api and ret_scrape_google == 10000:
        return {'error': 'No data found', 'error_type': 'No data'}
    if 'error' in ret_open_library or 'error' in ret_google_api or ret_scrape_google == 10000:
        ret['error'] = []
        ret['error_type'] = []

    if 'error' in ret_open_library:
        ret['error'].append(ret_open_library['error'])
        ret['error_type'].append(ret_open_library['error_type'])
    if 'error' in ret_google_api:
        ret['error'].append(ret_google_api['error'])
        ret['error_type'].append(ret_google_api['error_type'])
    if ret_scrape_google == 10000:
        ret['error'].append('No data found in Google search')
        ret['error_type'].append('No data')
    return ret


# metadata returns a dictionary with the metadata of the book
def find_book_open_library(title, author, print_results=False):
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
    
    if print_results:
        with open('metadata/single_results/open_library_results.txt', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    if 'docs' not in data:
        return ret

    docs = data['docs']

    for doc in docs:
        try:
            author_correct = False

            if 'author_name' in doc:
                author_correct = doc['author_name'][0].lower() in author.lower() or author.lower() in doc['author_name'][0].lower()
                
            if 'author_alternative_name' in doc:
                for author_alt in doc['author_alternative_name']:
                    author_correct = author_correct or author.lower() in author_alt.lower() or author_alt.lower() in author.lower()
                    if 'translator' in author_alt.lower() or 'translated by' in author_alt.lower():
                        print('Book is a translation')
                        continue

            if not ((doc['title'].lower() in title.lower() or title.lower() in doc['title'].lower()) and author_correct):
                print("Book not found in API")
                continue

            print("matching book found in API")

            if 'first_publish_year' in doc and doc['first_publish_year'] < ret['year'] and doc['first_publish_year'] != 1800:
                ret['year'] = doc['first_publish_year']

            if 'publish_date' in doc:
                for date in doc['publish_date']:
                    try:
                        if int(date) < ret['year'] and int(date) != 1800:
                            ret['year'] = int(date)
                    except:
                        pass

            if 'publish_year' in doc:
                for date in doc['publish_year']:
                    try:
                        if int(date) < ret['year'] and int(date) != 1800:
                            ret['year'] = int(date)  
                    except:  
                        pass       

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
    print(ret)
    return ret


def find_book_google_api(title, author, print_results=False):
    ret = {'year': 10000, 'place': [], 'first_sentence': []}  # starting with a year of 10000 so that found books can be less
    combined_title = title.replace(" ", "+")
    combined_author = author.replace(" ", "+")
    
    load_dotenv()
    api_key1 = os.getenv('GOOGLE_BOOKS_API_KEY')
    api_key2 = os.getenv('GOOGLE_BOOKS_API_KEY2')
    api_key3 = os.getenv('GOOGLE_BOOKS_API_KEY3')
    api_key4 = os.getenv('GOOGLE_BOOKS_API_KEY4')

    i = -1

    for api_key in [api_key1, api_key2, api_key3, api_key4]:
        i += 1
        url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{combined_title}+inauthor:{combined_author}+before:1950&key={api_key}'

        try:
            # Set a timeout value in seconds
            response = requests.get(url, timeout=10)
            
            # Check if the response was successful (status code 200)
            response.raise_for_status()
            data = response.json()
            print(url)
            break
        except Timeout as e:
            if i == 3:
                return {'error': str(e), 'error_type': 'Timeout'}
        except RequestException as e:
            if i == 3:
                return {'error': str(e), 'error_type': 'RequestException'}


    if print_results:
        with open('metadata/single_results/google_api_results.txt', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    if 'items' not in data:
        return ret
    
    items = data['items']

    for item in items:
        doc = item['volumeInfo']
        try:
            if doc['title'].lower() in title.lower() or title.lower() in doc['title'].lower():
                print("matching book found in API")
                date = int(doc['publishedDate'].split('-')[0])
                if date < int(ret['year']) and date != 101 and date != 1800:
                    try:
                        ret['year'] = date
                    except:
                        print("No year data")
        except:
            print("Error getting book information, skipping book in the list")

    print(ret)
    return ret


def get_scrape_google(title, author, print_results=False):
    dict = scrape_google.scrape_google(title, author)

    if print_results:
        with open('metadata/single_results/scrape_google_results.txt', 'w', encoding='utf-8') as file:
            json.dump(dict, file, indent=4)

    try:
        year = int(dict['year'].split(' ')[-1])
    except:
        year = 10000

    return year


if __name__ == "__main__":
    main()
