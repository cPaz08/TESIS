from scraper.scraper import Scrap_Selenium
from config import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    scrap_selenium = Scrap_Selenium(URL_BASE_ALIBABA)
    try:
        while True:
            try:
                scrap_selenium.scrape(f'{OUTPUT_ALIBABA}/dato_{scrap_selenium.page}.csv')
                
                if not scrap_selenium.next_button(OUTPUT_ALIBABA):
                    break  # Si no hay más páginas, termina el bucle
            except KeyboardInterrupt:
                print('🚨 Extracción de datos detenida por el usuario')
                break               
            except Exception as e:
                print('❌ ocurrió un error:', e)
                break # Sale del bucle cuando no hay más botones
    except KeyboardInterrupt:
        print('🚨 Extracción interrumpida manualmente.')
    finally:
        print("🔄 Cerrando WebDriver...")
        try:
            scrap_selenium.driver.quit()  # Asegura el cierre del WebDriver
            print("✅ WebDriver cerrado correctamente.")
        except Exception as e:
            print("⚠️ Error al cerrar WebDriver:", e)