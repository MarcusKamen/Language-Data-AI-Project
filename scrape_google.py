import requests
from bs4 import BeautifulSoup

def scrape_google(title, author):
    title = title.replace(" ", "+")
    author = author.replace(" ", "+")
    url = 'https://www.google.com/search?q=' + title + "+" + author
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
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

        print(f'{url}: ' + str(ret))
        print()
        return ret
    except Exception as e:
        print(f'{url}: ' + str(e))
        print()
        return {"error" : str(e)}

if __name__ == '__main__':
    scrape_google("The Spider","Fergus Hume")
    scrape_google("Uncle Silas", "J.S. Lefanu")
    scrape_google("The Secret Garden", "Frances Hodgson Burnett")
    scrape_google("A Popular History of France From The Earliest Times", "Francois Guizot")
    scrape_google("m", "n")
    scrape_google("The Lure of the Dim Trails", "by (AKA B. M. Sinclair) B. M. Bower")
    scrape_google("The Lure of the Dim Trails", "B. M. Bower")