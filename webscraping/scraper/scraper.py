import requests
import logging
from parser import *
from utils import *


def fetch_html(url):
    '''Obtiene el HTML de la página web.'''
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f'Página {url} descargada exitosamente.')
        return response.text
    
    except requests.exceptions.RequestException as e:
        logging.error(f'Error al descargar {url}: {e}')
        return None
    
def scrape(url, output_file):
    '''Ejecuta el proceso de scarping'''
    html = fetch_html(url)

    if html:
        data = parse_data_ml(html)
        save_to_csv(data, output_file)


if __name__ == '__main__':
    url = 'https://listado.mercadolibre.com.pe/incubadora-huevo-codorniz'
    html = fetch_html(url)
    data = parse_data_ml(html)

    print(data)
