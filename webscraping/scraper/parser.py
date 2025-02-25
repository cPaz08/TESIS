# scrapper/parser.py

from bs4 import BeautifulSoup
import re

def parse_data_ml(html):
    '''Parsea el HTML y extrae datos requeridos.'''
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('h3', class_='poly-component__title-wrapper')
    print(f"🔎 Se encontraron {len(products)} productos en la página.")  # Verifica cuántos productos detecta
    data = []
    keywords = ['nacedora', 'incubadora']

    for product in products:
        # product_text = product.a.text.lower()
        # print(f"📌 Producto encontrado: {product_text}")  # Verifica qué productos está leyendo

        if any(word in product.a.text.lower() for word in keywords):
            if re.search(r'codorniz', product.a.text, re.IGNORECASE):
                # print(product.a.get_text(strip=True))
                data.append({
                    'Nombre': product.a.get_text(strip=True),
                    'Url': product.a['href'],
                    'Precio': 'N/A'  # Se puede reemplazar con un valor real si se extrae del HTML
                })
                print(f"✅ Agregado: {product.a.get_text(strip=True)}")  # Muestra los productos agregados

    print(f"📊 Total de productos guardados en esta página: {len(data)}")
    return data

def parse_data_switch(html):
    '''Parsea el HTML y extrae datos requeridos.'''
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('li', class_='ui-search-layout__item shops__layout-item')
    data = []
    keywords = ['nintendo', 'switch']

    for product in products:
        # Buscar el título del producto
        title_tag = product.find('h3', class_='poly-component__title-wrapper')
        if not title_tag:
            continue
        
        link_tag = title_tag.find('a')
        if not link_tag:
            continue
        
        title = link_tag.get_text(strip=True).lower()

        # Filtrar productos que contengan 'nintendo' y 'switch' en el título
        if any(word in title for word in keywords):
            # Solo los que contienen 'lite'
            if not re.search(r'lite', title, re.IGNORECASE):
                continue

            # Buscar el precio
            monetary_unit_tag = product.find('span', class_='andes-money-amount__currency-symbol')
            monetary_unit = monetary_unit_tag.get_text(strip=True)if monetary_unit_tag else 'None/'
            price_tag = product.find('span', class_='andes-money-amount__fraction')
            price = price_tag.get_text(strip=True) if price_tag else "No disponible"

            data.append({
                'Nombre': link_tag.get_text(strip=True),
                'Precio': f'{monetary_unit} {price}',
                'Url': link_tag['href']
            })

    return data

def parse_data_alibaba(html):
    '''Parsea el HTML y extrae datos requeridos.'''
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('div', class_='traffic-card-gallery')
    data = []
    keywords = ['incubadora', 'nacedora']

    for product in products:
        # Buscar el título del producto
        title_tag = product.find('h2', attrs={"style":"display: inline;"})
        if not title_tag:
            continue
        
        link_tag = product.find('a')
        if not link_tag:
            continue
        
        title = title_tag.get_text(strip=True).lower()

        # Filtrar productos que contengan 'nintendo' y 'switch' en el título
        if any(word in title for word in keywords):
            # Solo los que contienen 'lite'
            if not re.search(r'codorniz', title, re.IGNORECASE):
                continue

            # Buscar el precio
            # monetary_unit_tag = product.find('span', class_='andes-money-amount__currency-symbol')
            # monetary_unit = monetary_unit_tag.get_text(strip=True)if monetary_unit_tag else 'None/'
            price_tag = product.find('div', attrs={"data-component":"ProductPrice"})
            price = price_tag.get_text(strip=True) if price_tag else "No disponible"

            data.append({
                'Nombre': title_tag.get_text(strip=True),
                'Precio': f'{price}',
                'Url': link_tag['href']
            })

    return data