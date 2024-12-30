import requests
from bs4 import BeautifulSoup
import csv

# URL of the IMDb top-rated movies page
URL = 'https://www.imdb.com/chart/top'

def get_page_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching the page: {response.status_code}")
        return None
    return response.content

def extract_movie_data(soup):
    movies = []
    movie_elements = soup.find_all('tr')  # Adjust if necessary
    if not movie_elements:
        print("No movie data found!")
        return movies

    for row in movie_elements:
        title_column = row.find('td', class_='titleColumn')
        if title_column is None:
            continue  # Skip rows without a title column

        title = title_column.a.text
        year = title_column.span.text.strip('()')
        director = title_column.a['title']
        rating = row.find('td', class_='ratingColumn').strong.text

        # Check if genres are available
        genre_column = row.find('span', class_='genre')
        genres = genre_column.text.strip() if genre_column else "N/A"

        movies.append({
            'Title': title,
            'Release Year': year,
            'Director': director,
            'Rating': rating,
            'Genres': genres
        })

    return movies

def save_to_csv(movies):
    if not movies:  # Check if the list is empty
        print("No movie data to save.")
        return

    keys = movies[0].keys()  # Get keys from the first dictionary
    with open('top_rated_movies.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(movies)

if __name__ == "__main__":
    html = get_page_html(URL)
    if html:
        print(html)  # Print the HTML content to inspect its structure
        soup = BeautifulSoup(html, 'html.parser')
        movies_data = extract_movie_data(soup)
        if not movies_data:
            print("No movie data found!")
        else:
            save_to_csv(movies_data)
            print("Top-rated movies data has been saved to 'top_rated_movies.csv'.")