from datetime import datetime
import requests
import csv
import bs4

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}

def get_page_html(url):
    res = requests.get(url=url, headers=REQUEST_HEADER)
    return res.content

def get_product_price(soup):
    price_span = soup.find('span', class_='price')  # Update the class based on actual HTML
    if price_span:
        price = price_span.text.strip().replace('KSh', '').replace(',', '')
        try:
            return float(price)
        except ValueError:
            print("Value Obtained For Price Could Not Be Parsed")
            return None
    return None

def get_product_title(soup):
    title = soup.find('h1', class_='product-title')  # Update the class based on actual HTML
    return title.text.strip() if title else None

def get_product_rating(soup):
    rating_div = soup.find('div', class_='rating')  # Update the class based on actual HTML
    if rating_div:
        rating_span = rating_div.find('span')
        return float(rating_span.text.strip()) if rating_span else None
    return None

def extract_product_info(url):
    product_info = {}
    print(f'Scraping URL: {url}')
    html = get_page_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    product_info['price'] = get_product_price(soup)
    product_info['title'] = get_product_title(soup)
    product_info['rating'] = get_product_rating(soup)
    return product_info

if __name__ == "__main__":
    products_data = []
    with open('carrefour_products_urls.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[0]
            products_data.append(extract_product_info(url))

    output_file_name = 'output-{}.csv'.format(datetime.today().strftime("%m-%d-%Y"))
    with open(output_file_name, 'w', newline='') as outputfile:
        writer = csv.writer(outputfile)
        if products_data:
            writer.writerow(products_data[0].keys())
            for product in products_data:
                writer.writerow(product.values())