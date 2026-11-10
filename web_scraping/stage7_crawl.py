# All scrapers start with the following template
#-----------------------------------------------
import requests
import time
from bs4 import BeautifulSoup

url =input("Enter URL:")

try:
    r = requests.get(url, timeout = 10)
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
    quit()

soup = BeautifulSoup(r.content, "html5lib")


#-----------------------------------------------

#7.1
raw = soup.select_one("li.col-xs-6" ).find_next("a")

print(raw["href"])

nxt = soup.select_one("li.next a")

print(nxt["href"])

#7.2
from urllib.parse import urljoin

page = "https://books.toscrape.com/"

print(urljoin(page, nxt["href"]))

base = "https://books.toscrape.com/"

url_from_homepage = base + "catalogue/page-2.html"   # next link as written on the homepage
url_from_page2 = base + "page-3.html"                # next link as written on page 2

print(url_from_homepage, requests.get(url_from_homepage, timeout=10).status_code)
print(url_from_page2, requests.get(url_from_page2, timeout=10).status_code)


#7.4

book_list = []

rating_list = {"One":1, "Two":2, "Three":3, "Four": 4, "Five": 5 }

url = "https://books.toscrape.com/"

def parse_book(book):
    url_temp = "https://books.toscrape.com/catalogue"
    link = book.select_one("h3 a")
    ttl = link.get("title")
    ref = urljoin(url_temp, link.get("href"))
    books_price = book.select_one("p.price_color")
    prc = float(books_price.text[1:])
    rating_tag = book.select_one("p.star-rating")
    rating = rating_list[rating_tag["class"][1]]
    record = {"Title":ttl, "Reference":ref, "Price": prc, "Rating": rating}
    return record

session = requests.Session()

while True:
    try:
        r = session.get(url, timeout = 10)
        r.raise_for_status()
    except session.exceptions.RequestException as e:
        print("Request failed:", e)
        break
    soup = BeautifulSoup(r.content, "html.parser")
    containers = soup.select("article.product_pod")
    for book in containers:
        book_list.append(parse_book(book))
    test = soup.select_one("li.next a")
    if test is None:
        break
    url = urljoin(url, test["href"])
    time.sleep(0.5)


print(len(book_list))

#7.5
