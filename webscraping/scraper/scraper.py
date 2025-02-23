from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import logging
from scraper.parser import *
from scraper.utils import *

class Scrap_Selenium:

    def __init__(self, url):
        options = Options()
        # options.add_argument("--headless")  
        # options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get(url)

    def fetch_html_selenium(self):
        '''Devuelve el HTML actual de la página.'''
        return self.driver.page_source
        
    def scrape(self, output_file):
        '''Ejecuta el proceso de scarping'''
        html = self.fetch_html_selenium()

        if html:
            data = parse_data_ml(html)
            save_to_csv(data, output_file)


if __name__ == '__main__':
    url = 'https://listado.mercadolibre.com.pe/incubadora-huevo-codorniz'
    url2 = 'https://listado.mercadolibre.com.pe/nintendo-switch#D[A:nintendo%20switch]'
    output_file = 'mercado_libre.csv'
    scrap_selenium = Scrap_Selenium(url)
    

    while True:
        try:
            html = scrap_selenium.fetch_html_selenium()
            data = parse_data_ml(html)
            save_to_csv(data, output_file)
            print(data)

            try:
                # Esperar a que aparezca el banner de cookies
                cookie_button = WebDriverWait(scrap_selenium.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Aceptar")]'))
                )
                cookie_button.click()
                print("Banner de cookies cerrado.")
            except:
                print("No se encontró el banner de cookies o ya está cerrado.")

            # Esperar que el notón "Siguiente" esté disponible
            next_button = WebDriverWait(scrap_selenium.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@title="Siguiente"]'))
            )
            next_button.click()

            # Esperar que la nueva página cargue antes de continuar
            WebDriverWait(scrap_selenium.driver, 5).until(
                EC.staleness_of(next_button) # Espera a que el botón se 'refresque'
            )
        except Exception as e:
            print('No hay más páginas disponibles o ocurrió un error:', e)
            break # Sale del bucle cuando no hay más botones
    
    scrap_selenium.driver.quit()
