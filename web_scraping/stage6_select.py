# All scrapers start with the following template
#-----------------------------------------------
import requests
from bs4 import BeautifulSoup

url =input("Enter URL:")

try:
    r = requests.get(url, timeout = 10)
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
    quit()

soup = BeautifulSoup(r.content, "html.parser")


#-----------------------------------------------
#6.1
containers = soup.select("li.col-xs-6") 

print(len(containers))

container = soup.select_one("li.col-xs-6")

print(container)

tag = soup.select("p.price_color")

price = [p.get_text(strip = True) for p in tag]

print(price)

nxt = soup.select("ul.nav-list ul a")
booklst = [p.get_text(strip = True) for p in nxt]

print(booklst)

#6.2

all_books = []

rating_list = {"One":1, "Two":2, "Three":3, "Four": 4, "Five": 5 }

def parse_book(book):
    link = book.select_one("h3 a")
    ttl = link.get("title")
    ref = link.get("href")
    books_price = book.select_one("p.price_color")
    prc = float(books_price.text[1:])
    rating_tag = book.select_one("p.star-rating")
    rating = rating_list[rating_tag["class"][1]]
    record = {"Title":ttl, "Reference":ref, "Price": prc, "Rating": rating}
    return record

#6.3
category_dict = dict()

books = soup.select("ul.nav-list a")[1:]

for book in books:
    key = book.get_text(strip =True)
    value = book["href"]
    category_dict[key] = value

print(category_dict)
    
