# Language-Data-AI-Project


## Getting Started

1. Pip install requests
```bash
pip install requests
```

2. Create empty data and metadata folders
```bash
python getting_started.py
```


2. Download data and place in raw folder from 
[Data](https://vanderbilt365-my.sharepoint.com/personal/marius_e_schueller_vanderbilt_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fmarius%5Fe%5Fschueller%5Fvanderbilt%5Fedu%2FDocuments%2FRawFiles%2Ezip&parent=%2Fpersonal%2Fmarius%5Fe%5Fschueller%5Fvanderbilt%5Fedu%2FDocuments&ga=1)


3. Clean the data and get the metadata
```bash
python clean_data_and_get_metadata.py
```



4. download nltk

pip install nltk

5. get the word counts of all stemmed and lemmatized data.

python word_counts.py



## Explanation of Metadata files

1. metadata.csv - Found full metadata for this file, including first sentence
2. nofirstsentence.csv - Found full metadata for this file, not including first sentence
3. booksnotfound.csv - Did not find any metadata for this file
4. wrongstars.csv - File is not formatted well to search for first sentence and pull cleaned information
5. nostartdata.csv - File does not have necessary starter information to be considered (e.g. it is a translation)



