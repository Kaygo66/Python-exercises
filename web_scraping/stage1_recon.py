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
text = soup.get_text()  #returns only the human-readable text from the entire HTML document or a given tag. 
print(text.count("£"), text.count("Â£"))
#r.encoding = "utf-8"



#-----------------------------------------------
#print(r.status_code)
print(r.headers)
#print(r.encoding)
#print(r.apparent_encoding)
print(soup.title.get_text(strip = True))

print(r.text)

