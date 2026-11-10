# =============================================================================
# Code written by Kaygo66, AI was used to generate the comments.
# Bookshop pricing report
# Crawls every listing page of books.toscrape.com, saves the full catalogue
# to books.csv, and prints a summary report for the shop owner.
# =============================================================================

import csv                          # writing the CSV file
import time                         # pausing between requests
from pathlib import Path            # building a file path next to this script
from urllib.parse import urljoin    # turning relative links into full URLs

import requests                     # fetching web pages
from bs4 import BeautifulSoup       # parsing HTML

# --- Constants: values set once and never changed ----------------------------

START_URL = "https://books.toscrape.com/"

# The star rating is stored as a word in a class name ("star-rating Three"),
# so this dictionary converts the word into a number with a single lookup.
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


# -----------------------------------------------------------------------------
# get_soup: fetch one page and return it as a BeautifulSoup object
# -----------------------------------------------------------------------------
def get_soup(url, session):
    try:
        # The session reuses one open connection for every page (faster
        # than opening a new connection with requests.get each time).
        r = session.get(url, timeout=10)
        r.raise_for_status()        # turn 404, 500 etc. into an exception
    except requests.exceptions.RequestException as e:
        # Covers every requests error: no connection, timeout, bad status...
        print("Request failed:", e)
        return None                 # signal failure; the caller decides what to do

    # Pass the raw bytes (r.content), so BeautifulSoup detects the encoding
    # itself and the £ signs come out correctly.
    return BeautifulSoup(r.content, "html.parser")


# -----------------------------------------------------------------------------
# parse_book: turn ONE book container into a dictionary
# page_url is the page the book was found on, needed to resolve its link
# -----------------------------------------------------------------------------
def parse_book(book, page_url):
    # Every search starts from `book`, so it only looks inside this one book.
    link = book.select_one("h3 a")

    # The link's text is shortened ("A Light in the ..."); the full title
    # is stored in its title attribute.
    title = link.get("title")

    # The href is relative, and its meaning depends on the page it came from,
    # so it is resolved against that page to get a full, clickable URL.
    ref = urljoin(page_url, link.get("href"))

    # "£51.77" -> slice off the £ sign -> 51.77 as a number
    price = float(book.select_one("p.price_color").text[1:])

    # class comes back as a list, e.g. ['star-rating', 'Three'];
    # index 1 is the rating word, which RATINGS converts to a number.
    rating_tag = book.select_one("p.star-rating")
    rating = RATINGS[rating_tag["class"][1]]

    return {"Title": title, "Reference": ref, "Price": price, "Rating": rating}


# -----------------------------------------------------------------------------
# crawl: follow the "next" links from start_url until the last page,
# collecting every book on the way. Returns a list of dictionaries.
# -----------------------------------------------------------------------------
def crawl(start_url, session):
    books = []
    url = start_url                 # address of the page currently being processed
    page = 0

    while True:                     # we don't know the page count in advance
        page += 1

        # --- once per page ---
        soup = get_soup(url, session)
        if soup is None:            # the request failed: stop, keep what we have
            break

        for book in soup.select("article.product_pod"):
            # --- once per book ---
            books.append(parse_book(book, url))

        print(f"Page {page}: {len(books)} books so far")

        # Guard clause: the last page has no "next" link, so the loop ends.
        next_link = soup.select_one("li.next a")
        if next_link is None:
            break

        # The new address replaces the old one. The OLD url is used as the
        # base, because the link was found on the page we just processed.
        url = urljoin(url, next_link["href"])

        time.sleep(0.5)             # be polite: pause between requests

    return books


# -----------------------------------------------------------------------------
# save_csv: write the list of book dictionaries to a CSV file
# -----------------------------------------------------------------------------
def save_csv(books, filename):
    # "w"                   creates the file, or overwrites it if it exists
    # newline=""            prevents blank lines between rows on Windows
    # encoding="utf-8-sig"  lets Excel display £ and accents correctly
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        # fieldnames must match the dictionary keys exactly (capitals included)
        writer = csv.DictWriter(f, fieldnames=["Title", "Reference", "Price", "Rating"])
        writer.writeheader()        # first line: the column names
        writer.writerows(books)     # one line per dictionary


# -----------------------------------------------------------------------------
# report: print the owner's summary
# -----------------------------------------------------------------------------
def report(books):
    # --- Count books and add up prices for each rating ---
    counts = {}                     # rating -> number of books
    totals = {}                     # rating -> sum of their prices
    for book in books:
        rating = book["Rating"]
        counts[rating] = counts.get(rating, 0) + 1
        totals[rating] = totals.get(rating, 0) + book["Price"]

    # --- Overall figures ---
    print("\nTotal books:", len(books))
    print("Overall average price:", round(sum(totals.values()) / len(books), 2))

    # --- Count and average price per rating ---
    # {value:>6} right-aligns a value in 6 characters, so the columns line up.
    print("\nRating  Books  Avg price")
    for rating in sorted(counts):   # sorted() on a dictionary gives its keys in order
        avg = round(totals[rating] / counts[rating], 2)
        print(f"{rating:>6}  {counts[rating]:>5}  {avg:>9}")

    # --- Five best-value books: five-star only, cheapest first ---
    # Filter, then sort by price with a lambda, then take the first five.
    five_star = [b for b in books if b["Rating"] == 5]
    print("\nBest value five-star books:")
    for book in sorted(five_star, key=lambda b: b["Price"])[:5]:
        print(f"  £{book['Price']:.2f}  {book['Title']}")

    # --- Most expensive book ---
    # max() returns the whole dictionary; the lambda only decides what to compare.
    top = max(books, key=lambda b: b["Price"])
    print(f"\nMost expensive: {top['Title']} at £{top['Price']:.2f}")


# =============================================================================
# Main: everything above only DEFINES functions; this is what actually runs
# =============================================================================
session = requests.Session()        # created once, shared by every request
books = crawl(START_URL, session)
save_csv(books, Path(__file__).parent / "books.csv")   # saved next to this script
report(books)
