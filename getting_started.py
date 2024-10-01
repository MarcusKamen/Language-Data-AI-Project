import os

def main():
    path = './data'

    os.makedirs(path, exist_ok=True)
    os.makedirs(path+'/raw', exist_ok=True)
    os.makedirs(path+'/raw_clean', exist_ok=True)

    os.makedirs('./metadata', exist_ok=True)


if __name__ == "__main__":
    main()
