import os

# specify the path for the directory – make sure to surround it with quotation marks
path = './data'

# create new single directory
os.mkdir(path)
os.mkdir(path+'/.mirror')
os.mkdir(path+'/counts')
os.mkdir(path+'/raw')
os.mkdir(path+'/text')
os.mkdir(path+'/tokens')

os.mkdir('./metadata')
os.mkdir('./metadata/bookshelves_html')


