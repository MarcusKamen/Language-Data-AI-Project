import requests
from bs4 import BeautifulSoup

def scrape_google(title, author):
    title = title.replace(" ", "+")
    author = author.replace(" ", "+")
    response = requests.get('https://www.google.com/search?q=' + title + "+" + author)
    soup = BeautifulSoup(response.text, 'html.parser')

    key_info = soup.select(".BNeawe.tAd8D.AP7Wnd")
    author_raw = key_info[0].text
    by_index = author_raw.find("by")

    ret = {"author":author_raw[by_index+3:], "year":key_info[1].text}
    
    span = soup.find("span", class_="lU7jec")

    if span:
        h3 = span.find("h3", class_="zBAuLc l97dzf")
        
        if h3:
            div = h3.find("div", class_="BNeawe")
            
            if div:
                ret["title"] = div.get_text()

    print("Google found this information: " + str(ret))
    return ret

if __name__ == '__main__':
    scrape_google("The Spider","Fergus Hume")
    scrape_google("Uncle Silas", "J.S. Lefanu")
    scrape_google("The Secret Garden", "Frances Hodgson Burnett")
    scrape_google("A Popular History of France From The Earliest Times", "Francois Guizot")
    scrape_google("m", "n")