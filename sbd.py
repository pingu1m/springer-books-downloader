#! /usr/bin/env python3
import re
import random
import pandas as pd
import argparse
import requests
from bs4 import BeautifulSoup


def sb_list(books):
    """List books with specified keyword"""
    for book_title in books['title']:
        print(book_title)


def sb_download(word):
    """Download books with specified keyword"""
    for book_url in filtered_books['url']:

        page = requests.get(book_url)

        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            print(f"Downloading {soup.title.string}  | URL: {book_url} ...")
            book_links = soup.find_all('a', class_='test-bookpdf-link')

            book_link = book_links[0]
            pdf_link = 'https://link.springer.com' + book_link.attrs['href']

            filename = str(random.randint(1, 1000000)) + '_'.join(
                [word.strip() for word in soup.title.string.split()[0:-2]]) + '.pdf'
            print(filename)
            download_file(pdf_link, 'books/' + filename)

        else:
            raise Exception("Something went wrong")


def download_file(url, filename):
    local_filename = filename
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename


if __name__ == '__main__':
    xl_file = pd.ExcelFile('books.xlsx')
    sheet_name = xl_file.sheet_names.pop()
    books_uncleaned = xl_file.parse(sheet_name)
    books = books_uncleaned[['Book Title', 'Author', 'English Package Name', 'OpenURL']]
    books.columns = ['title', 'author', 'category', 'url']

    parser = argparse.ArgumentParser(description='Search or Download available books from Springer')

    parser.add_argument('keywords', metavar='N', type=str, nargs='+',
                        help='Keywords to search available books')

    parser.add_argument('--action', default="list",
                        help='Available actions are "list", "download". Defailt action is list')

    args = parser.parse_args()

    if args.action:
        if args.action not in ['list', 'download']:
            raise ValueError("Invalid Action entered.")

    keywords_regex = '|'.join([word.strip() for word in args.keywords])
    print(keywords_regex)
    does_title_contain_keywords = books.title.str.contains(keywords_regex, flags=re.IGNORECASE, regex=True)
    filtered_books = books[does_title_contain_keywords]

    for word in args.keywords:
        if args.action == 'list':
            sb_list(filtered_books)

        elif args.action == 'download':
            sb_download(filtered_books)
