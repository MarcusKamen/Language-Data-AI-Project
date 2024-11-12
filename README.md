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

pip install scikit-learn

pip install pandas openpyxl

5. get the word counts of all stemmed and lemmatized data.

python word_counts.py

6. ridge regression baby

python ridge_regression_predict.py

//with 5000 documents downloaded
Mean Squared Error: 9412.832333371905

Example Predictions (True Date vs Predicted Date):
True Date: 1776, Predicted Date: 1823
True Date: 1915, Predicted Date: 1970
True Date: 1895, Predicted Date: 1899
True Date: 1885, Predicted Date: 1900
True Date: 1914, Predicted Date: 1829


## Explanation of Metadata files

1. metadata.csv - Found full metadata for this file, including first sentence
2. nofirstsentence.csv - Found full metadata for this file, not including first sentence
3. booksnotfound.csv - Did not find any metadata for this file
4. wrongstars.csv - File is not formatted well to search for first sentence and pull cleaned information
5. nostartdata.csv - File does not have necessary starter information to be considered (e.g. it is a translation)

Interestingly, google search fails on this:
Hyacinth,George A. Birmingham


Intesteresting books that have bad data but our model does better:

49045-0.txt,1200,1895.8853209767926,The Expositor's Bible: The Book of Deuteronomy,Andrew Harper
Actually written 1903

6038.txt,1200,1898.5478497655572,The Great Doctrines of the Bible,Rev. William Evans
Actually written 1912

## Results

Input the model you would like to use and save all results (svm / ridge / neural): svm
Pearson correlation coefficient (r): 0.64

