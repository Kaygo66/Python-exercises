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

soup = BeautifulSoup(r.content, "html5lib")


#-----------------------------------------------
#5.1
books = soup.find_all("li", class_= "col-xs-6 col-sm-4 col-md-3 col-lg-3" )

all_books = []

rating_list = {"One":1, "Two":2, "Three":3, "Four": 4, "Five": 5 }

for book in books:
    link = book.find("h3").find("a")
    ttl = link.get("title")
    ref = link.get("href")
    books_price = book.find("p", class_ = "price_color")
    prc = float(books_price.text[1:])
    rating_tag = book.find("p", class_ = "star-rating")
    rating = rating_list[rating_tag["class"][1]]
    record = {"Title":ttl, "Reference":ref, "Price": prc, "Rating": rating}
    all_books.append(record)

for element in all_books:
    print(element)

#5.3


def parse_book(book):
    link = book.find("h3").find("a")
    ttl = link.get("title")
    ref = link.get("href")
    books_price = book.find("p", class_ = "price_color")
    prc = float(books_price.text[1:])
    rating_tag = book.find("p", class_ = "star-rating")
    rating = rating_list[rating_tag["class"][1]]
    record = {"Title":ttl, "Reference":ref, "Price": prc, "Rating": rating}
    return record



#part_B
#5.4
book_info = dict()

rows = soup.find("table", class_ = "table table-striped").find("tbody").find_all("tr")

for row in rows:
    key = row.find("th").get_text(strip = True)
    value = row.find("td").get_text(strip = True)
    book_info[key] = value

print(book_info)

#5.5

av = book_info["Availability"]

start = av.find("(")
end = av.find("a")

print(av[start + 1:end])

#5.6

bc = soup.find("ul", class_ = "breadcrumb").find_all("li")

categ = bc[2]

print(categ.get_text(strip = True))

#5.7
ds = soup.find("div", id="product_description").find_next("p")

print(ds.get_text(strip = True))

