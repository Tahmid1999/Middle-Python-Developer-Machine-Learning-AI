import requests

def fetch_book_info(isbn):
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')

    if response.status_code == 200:
        data = response.json()

        if 'items' in data:
            book_info = data['items'][0]['volumeInfo']

            print(f"Title: {book_info['title']}")
            print(f"Authors: {', '.join(book_info['authors'])}")
            print(f"Publisher: {book_info['publisher']}")
            print(f"Published Date: {book_info['publishedDate']}")
        else:
            print("No book found with this ISBN.")
    else:
        print(f"Error: {response.status_code}")

fetch_book_info('9780140449136')


