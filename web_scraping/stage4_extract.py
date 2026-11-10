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
#4.1
books = soup.find("li", class_= "col-xs-6 col-sm-4 col-md-3 col-lg-3" )
books_num = books.find("h3").find("a")
name = books_num.get("title")

print(name)
print(books_num.get_text())

#4.2
print(books_num.get("href"))
print(books_num["href"])   # this one does not return None and gives a KeyError thus stopping the code if the attribute is missing

#4.3
books_price = books.find("p", class_ = "price_color")
print(books_price.text)
print(float(books_price.text[1:]))

#4.3
rating_tag = books.find("p", class_ = "star-rating")
#print(rating_tag["class"])
#print(rating_tag.attrs)

rating_list = {"One":1, "Two":2, "Three":3, "Four": 4, "Five": 5 }

print(rating_list[rating_tag["class"][1]])


#4.5
books_stock = books.find("p", class_ = "instock availability")
print(books_stock.get_text(strip = True))


