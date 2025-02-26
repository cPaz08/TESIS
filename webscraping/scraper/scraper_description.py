import requests
from bs4 import BeautifulSoup
from scraper.utils import process_csv_files

class Scraper_description:
    def __init__(self, data_path):
        self.data_path = data_path        

    def get_product_description(self, url):
        """
        Extrae la descripción de un producto desde su URL
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Wind64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        SELECTORS = {
            "mercado": ("p", {"class": "ui-pdp-description__content"}),
            "alibaba": ("div", {"class": "module_product_specification"}),
            "switch": ("div", {"class": "module_product_specification"})
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            for site, tuple in SELECTORS.items():
                if site in self.data_path.lower():
                    tag, attrs = tuple
                    descripcion_tag = soup.find(tag, attrs) # Encuentra la etiqueta con los atributos dinámicos
                else:                    
                    print(f'No se encontró las etiquetas para el archivo {self.data_path}.')
            
            if descripcion_tag:
                return descripcion_tag.get_text(strip=True)
            else:
                return 'Descripción no encontrada'
        except requests.RequestException as e:
            return f'Error al obtener la página: {e}'