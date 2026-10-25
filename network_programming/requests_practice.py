# fetch a web page and print its 10 most common words

import requests

req = input("enter a url:")


try:
    r = requests.get(req, timeout=10)
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
    quit()

print(r.status_code)
print(r.headers["Content-Type"])

dct = dict()

words = r.text.split()

for word in words:
    dct[word] = dct.get(word, 0) +1

top = sorted(dct.items(), key=lambda item: item[1], reverse=True)[:10]
for word, count in top:
    print(word, count)

