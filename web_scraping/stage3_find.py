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

containers = soup.find_all("article", class_ = "product_pod") # the <li attribute with the specific class that defines book containers

first_book = soup.find("article", class_= "product_pod")

price = soup.find_all("p", class_="price_color")

test = soup.find("li", class_="previous")

sidebar = soup.find("ul", class_ = "nav nav-list")
books = sidebar.find("ul")
categ = books.find_all("li")


#print(len(containers))
#print(first_book.prettify())
#print(len(price))

#print(test.text())

#print(len(category_num))

print(len(categ))