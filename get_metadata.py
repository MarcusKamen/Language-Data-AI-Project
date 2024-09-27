import requests

# for each book

# Create a call that will


title = input("Input the title: ").strip()

author = input("Input the author: ").strip()

combined = (title.replace(" ", "+") + "+" +author.replace(" ", "+"))

url = "https://openlibrary.org/search.json?q=" + combined

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
        if doc['title'].lower() == title.lower() and doc['author_name'][0].lower() == author.lower():
            print("matching book found")
            # title: doc['title']
            # author name (list): doc['author_name']
            # publish year (also sometimes not listed): doc['first_publish_year']
            # place (sometimes not listed): doc['place'] 


            print(doc['first_publish_year'])
            #print(doc['place'])
    except:
        print("Error getting book information, skipping book in the list")



# TODO:
# Put data into csv file
# Account for weird author attributions in pg