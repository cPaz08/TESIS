import requests
from bs4 import BeautifulSoup
from scraper.utils import *
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

class Scraper_description:
    def __init__(self, data_path):
        print("🚀 Inicializando el scraper...")
        self.data_path = data_path
        self.driver = self._initialize_webdriver()
        self.index = 0
    
    def _initialize_webdriver(self):
        print("🖥️ Configurando WebDriver...")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    def close_driver(self):
        if self.driver:
            print("🔄 Cerrando WebDriver...")
            self.driver.quit()      
            print("✅ WebDriver cerrado correctamente.")

    def get_product_description(self, url):
        """
        Extrae la descripción de un producto desde su URL
        """
        if not url or not isinstance(url, str):
            print(f"⚠️ URL inválida: {url}")
            return "URL inválida"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Wind64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        SELECTORS = {
            'mercado': ("p", {"class": "ui-pdp-description__content"}),
            'alibaba': ("div", {"id": "J-rich-text-description"}),
            'switch': ("div", {"class": "module_product_specification"})
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            # Guardar el HTML en un archivo .txt
            # with open("output.html", "w", encoding="utf-8") as file:
            #     file.write(soup.prettify())

            # print("✅ Archivo guardado como output.html. Ábrelo para revisar el contenido.")

            sitio_detectado = None
            for site, (tag, attrs) in SELECTORS.items():
                if site in url.lower():
                    sitio_detectado = site
                    break  # Se detiene en el primer sitio coincidente
            
            if not sitio_detectado:
                print(f"⚠️ No se detectó el sitio para la URL: {url}")
                return "Sitio no reconocido"
            tag, attrs = SELECTORS[sitio_detectado]
            descripcion_tag = soup.find(tag, attrs)
            
            if descripcion_tag:
                    return descripcion_tag.get_text(" ", strip=True) 
            else:
                print(f"⚠️ No se encontró la descripción en {url}")
                return "Descripción no encontrada"

        except requests.RequestException as e:
            print(f"❌ Error al obtener la página {url}: {e}")
            return f"Error: {e}"
    
    def process_csv_url(self):
        if not os.path.exists(self.data_path):
            print(f"❌ La ruta {self.data_path} no existe.")
            return
        for file in os.listdir(self.data_path):
            if file.endswith(".csv"):
                file_path = os.path.join(self.data_path, file)
                print(f"📂 Procesando {file_path}...")
                try:
                    df = pd.read_csv(file_path)
                    if "Url" not in df.columns:
                        print(f"⚠️ El archivo {file} no contiene una columna 'Url'.")
                        continue
                    for index, row in df.iterrows():
                        url = row["Url"]
                        title = str(row['Nombre']) if pd.notna(row['Nombre']) else "sin_nombre"
                        description, img_urls = self.get_alibaba_description_and_img_urls(url)
                        try:
                            # Guardar en un archivo .txt
                            txt_file_name = f"{self.index}_{sanitize_filename(title)}.txt"  # Puedes cambiarlo para que sea más descriptivo
                            out_put_dir = save_description_to_txt(description, self.data_path, txt_file_name)
                            download_img(img_urls, out_put_dir)
                            self.index += 1
                        except Exception as e:
                            print(f"❌ Error {file}, fila{index}: {e}")
                            continue  
                except Exception as e:
                    print(f"❌ Error al leer {file}: {e}")
                    continue                     
              
    def get_alibaba_description_and_img_urls(self, url):
        print(f"🌐 Accediendo a la URL: {url}")
        self.driver.get(url)
        time.sleep(5)
        print("⏳ Esperando que la página cargue...")
        image_urls = []
        
        try:
            description_element = self.driver.find_element(By.ID, "J-rich-text-description")
            # Encontrar imágenes en la página
            imagenes = self.driver.find_elements(By.TAG_NAME, "img")
            # Extraer y mostrar las URLs de las imágenes
            image_urls = [img.get_attribute("src") for img in imagenes if img.get_attribute("src")]
            if description_element:
                print("✅ Descripción e imégenes encontradas")
                return description_element.text.strip(), image_urls
            else:
                print("⚠️ No se encontró la descripción o imágenes")
                return "Descripción no encontrada", image_urls
        except KeyboardInterrupt:
                print('🚨 Extracción de datos detenida por el usuario')
        except Exception as e:
            print(f"❌ Error al extraer la descripción: {e}")
            return "Descripción no encontrada", image_urls
           
if __name__ == '__main__':
    print("🚀 Iniciando proceso de scraping...")
    scraper = Scraper_description('data')
    try:
        url = "https://spanish.alibaba.com/product-detail/Best-Design-560-Egg-Incubator-For-62306155350.html"
        print(scraper.get_alibaba_description_and_img_urls(url))
    except KeyboardInterrupt:
        print("🚨 Extracción interrumpida manualmente.")
    finally:
        scraper.close_driver()
