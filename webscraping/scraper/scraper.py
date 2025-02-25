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

        # Intentar aceptar las cookies (modifica el XPATH según la web)
        try:
            cookie_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Aceptar")]'))
            )
            cookie_button.click()
            print("✅ Cookies aceptadas correctamente")
        except Exception as e:
            print("⚠ No se encontró el botón de cookies o ya estaban aceptadas:", e)

        self.page = 1

    def fetch_html_selenium(self):
        '''Devuelve el HTML actual de la página.'''
        return self.driver.page_source
        
    def scrape(self, output_file):
        '''Ejecuta el proceso de scarping'''
        print(f"🌍 Extrayendo datos de: {self.driver.current_url}")
        html = self.fetch_html_selenium()

        # Diccionario de parsers por palabra clave en el nombre del archivo
        parsers = {
            'mercado': parse_data_ml,
            'switch': parse_data_switch,
            'alibaba': parse_data_alibaba
        }

        # Buscar el parser adecuado según el nombre del archivo
        parse_function = None
        for keyword, func in parsers.items():
            if keyword in output_file.lower(): # Ignora mayúsculas/minúsculas
                parse_function = func
                break # Salir del bucle al encontrar el primer match
        
        if parse_function:
            # print(f"📄 Longitud del HTML: {len(html)} caracteres")
            # print(f"🔍 Vista previa HTML:\n{html[:1000]}")  # Muestra los primeros 500 caracteres
            data = parse_function(html)
            save_to_csv(data, output_file)
        else:
            print(f'No se encontró un parser para el archivo {output_file}.')

    def next_button(self, output_file):
        '''Hace clic en el botón "Siguiente" si está disponible'''
        buttons = {
            'mercado': '//a[@title="Siguiente"]',
            'switch': '//a[@title="Siguiente"]',
            'alibaba': '//a[@aria-label="Go to next page"]'
        }
        link_button = ''
        for keyword, link in buttons.items():
            if keyword in output_file.lower():
                link_button = link
                break
        
        try:
            current_url = self.driver.current_url  # Guardar la URL actual antes de hacer clic
            next_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, link_button))
            )
            next_button.click()

            # Esperar hasta que la URL cambie (si cambia)
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.current_url != current_url
            )

            # Esperar que la nueva página cargue antes de continuar
            # WebDriverWait(self.driver, 5).until(
            #     EC.staleness_of(next_button)
            # )

            self.page += 1
            print(f"➡ Avanzando a la página {self.page}")
            return True
        except Exception as e:
            print("🚫 No hay más páginas o ocurrió un error:", e)
            return False
    
    def close(self):
        '''Cierra el navegador'''
        self.driver.quit()



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
