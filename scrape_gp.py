import requests, bs4, zipfile, io, os

get_links = input("Get links (y/n) ")

if (get_links == "y"):
    count = 0
    os.remove("data/data_links.txt")
    f = open("data/data_links.txt", "a")

    # Starter page, could add what languages to download input
    page_url = "https://www.gutenberg.org/robot/harvest?offset=3860100&filetypes[]=txt&langs[]=en"
    while page_url != "https://www.gutenberg.org/robot/":
        print(str(count) + " book links stored!")
        response = requests.get(page_url)
        page_url = "https://www.gutenberg.org/robot/"

        # print(response.text)

        page_bs = bs4.BeautifulSoup(response.text, "lxml")

        for link in page_bs.find_all('a'):
            link_text = str(link.get('href'))
            if "http:" in link_text:
                f.write(link_text + "\n")
                count += 1
            else:
                page_url += link_text



    print("All Book Links Scraped!")
    f.close()

download_links = input("Download books (y/n) ")
if download_links == "y":
    download_all = input("Download all (y/n) ")
    if download_all == "y":
        amount = 100_000 # hard upper limit
    else:
        amount = int(input("How many books to download? "))

    f = open("data/data_links.txt", "r")

    count = 0
    line = f.readline().strip()
    while line != "" and count < amount:
        response = requests.get(line)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall("data/raw/")

        line = f.readline().strip()
        count += 1
        print(str(count) + " books downloaded!")
    f.close()

# Need to add metadata for each file
