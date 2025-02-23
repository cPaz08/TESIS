# scrapper/parser.py

from bs4 import BeautifulSoup
import re

def parse_data_ml(html):
    '''Parsea el HTML y extrae datos requeridos.'''
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('h3', class_='poly-component__title-wrapper')
    product_name = ['Nombre']
    product_url = ['Url']
    keywords = ['nacedora', 'incubadora']

    for product in products:
        if any(word in product.a.text.lower() for word in keywords):
            if re.search(r'codorniz', product.a.text, re.IGNORECASE):
                # print(product.a.get_text(strip=True))
                product_name.append(product.a.get_text(strip=True))
                product_url.append(product.a['href'])

    data = dict(zip(product_name, product_url))

    return data
