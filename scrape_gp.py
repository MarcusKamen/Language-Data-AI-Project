import requests, bs4

count = 0

f = open("data/data_links.txt", "a")

# Starter page, could add what languages to download input
page_url = "https://www.gutenberg.org/robot/harvest?offset=3860100&filetypes[]=txt&langs[]=en"
while page_url != "https://www.gutenberg.org/robot/":
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

    print(str(count) + " books stored!")

print("No More Pages!")
f.close()

# Need to download all the files


# Need to add metadata for each file
