from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import logging
from parser import *
from utils import *

class Scrap_Selenium:

    def __init__(self, url):
        self.url = url

    def fetch_html_selenium(self, url):
        '''Obtiene el HTML de la página usando Selenium.'''
        options = Options()
        # options.add_argument("--headless")  
        # options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            self.driver.get(url)
            time.sleep(3)

            page_source = self.driver.page_source # Extraemos el HTML después de que se cargue
            logging.info(f'Página {url} descargada exitosamente con Selenium')
            return page_source
        
        except Exception as e:
            logging.error(f'Error con Selenium {url}: {e}')
            return None
        # finally:
        #     driver.quit()
        
    def scrape(self, url, output_file):
        '''Ejecuta el proceso de scarping'''
        html = self.fetch_html_selenium(url)

        if html:
            data = parse_data_ml(html)
            save_to_csv(data, output_file)


if __name__ == '__main__':
    url = 'https://listado.mercadolibre.com.pe/incubadora-huevo-codorniz'
    scrap_selenium = Scrap_Selenium(url)
    html = scrap_selenium.fetch_html_selenium(url)
    data = parse_data_ml(html)
    print(data)

    while True:
        try:
            next_button = scrap_selenium.driver.find_element(By.XPATH, '//a[@title="Siguiente"]')
            next_button.click()
            time.sleep(3)
            data = parse_data_ml(html)
            print(data)
        except:
            print('No hay más páginas disponibles.')
            break # Sale del bucle cuando no hay más botones
    
    scrap_selenium.driver.quit()
