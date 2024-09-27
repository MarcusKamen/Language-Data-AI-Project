import os

def main():
    path = './data'

    os.makedirs(path, exist_ok=True)
    os.makedirs(path+'/.mirror', exist_ok=True)
    os.makedirs(path+'/counts', exist_ok=True)
    os.makedirs(path+'/raw', exist_ok=True)
    os.makedirs(path+'/text', exist_ok=True)
    os.makedirs(path+'/tokens', exist_ok=True)
    os.makedirs(path+'/raw_clean', exist_ok=True)

    os.makedirs('./metadata', exist_ok=True)
    os.makedirs('./metadata/bookshelves_html', exist_ok=True)


if __name__ == "__main__":
    main()
