from scraper.scraper import Scrap_Selenium
from config import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    scrap_selenium = Scrap_Selenium(URL_BASE_MERCADO_LIBRE)
    i = 1
    while True:
        try:
            scrap_selenium.scrape(f'{OUTPUT_MERCADO_LIBRE_DATA}//mercado_libre_{i}.csv')

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
            i += 1
        except Exception as e:
            print('No hay más páginas disponibles o ocurrió un error:', e)
            break # Sale del bucle cuando no hay más botones
    
    scrap_selenium.driver.quit()