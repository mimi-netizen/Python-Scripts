import requests
from bs4 import BeautifulSoup
import csv

# Sample URL of the Z-Library book listing page
URL = 'https://z-lib.fm/'  # Replace with a specific page if needed

def get_book_details():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all book containers (modify the selector as needed)
    book_containers = soup.find_all('div', class_='book-container')  # Update this class based on actual HTML

    books = []
    
    for book in book_containers:
        title = book.find('h2', class_='title').text.strip()  # Modify as needed
        author = book.find('p', class_='author').text.strip()  # Modify as needed
        genre = book.find('span', class_='genre').text.strip()  # Modify as needed
        price = book.find('p', class_='book-price').text.strip()  # Modify as needed
        
        books.append({
            'Title': title,
            'Author': author,
            'Genre': genre,
            'Price': price
        })

    return books

def save_to_csv(books):
    keys = books[0].keys()
    with open('zlibrary_books.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(books)

if __name__ == "__main__":
    book_details = get_book_details()
    if book_details:
        save_to_csv(book_details)
        print("Book details extracted and saved to zlibrary_books.csv")
    else:
        print("No book details found.")
        
