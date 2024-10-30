import requests
from tabulate import tabulate
from bs4 import BeautifulSoup
import re
import json


def get_books():
    url = "https://books.toscrape.com/"
    headers = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.ok:
        soup = BeautifulSoup(response.content, features="html.parser")
        product_pod = soup.find_all("article", class_="product_pod")
        book_regex = r'">([\w\s]+)<\/a>'
        books = re.findall(book_regex, str(product_pod))
        price = soup.find_all("p", class_="price_color")
        price_regex = r'">(.\d+.\d+)<\/p>'
        prices = re.findall(price_regex, str(price))
        data = zip(books, prices)
        return data

    return False


def get_books_text():
    data = get_books()
    if data:
        with open("books.txt", "w") as f:
            f.write("Books :\n")
            table = tabulate(
                data,
                headers=["Books", "Price"],
                tablefmt="fancy_grid",
            )
            f.write(table)


def get_books_json():
    data = get_books()
    if data:
        books_map = [{"book_name": book, "book_price": price}
                     for book, price in data]
        with open("books.json", "w") as f:
            json_books = json.dump(books_map, f, ensure_ascii=False)


if __name__ == "__main__":
    get_books_text()
    get_books_json()
