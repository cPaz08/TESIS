import requests
from bs4 import BeautifulSoup
from utils import *
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
        self.data_path = data_path        

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
    
    def process_csv_files(self):
        if not os.path.exists(self.data_path):
            print(f"❌ La ruta {self.data_path} no existe.")
            return
        for file in os.listdir(self.data_path):
            if file.endswith(".csv"):
                file_path = os.path.join(self.data_path, file)
                print(f"📂 Procesando {file_path}...")

                try:
                    df = pd.read_csv(file_path)
                except Exception as e:
                    print(f"❌ Error al leer {file}: {e}")
                    continue
                if "Url" not in df.columns:
                    print(f"⚠️ El archivo {file} no tiene una columna 'Url'.")
                    continue
                
                print("🔍 Extrayendo descripciones...")
                # df["description"] = df["Url"].apply(self.get_alibaba_description)

                # print("💾 Guardando archivo actualizado...")
                # save_description_to_csv(df, self.data_path, file)
                for index, row in df.iterrows():
                    url = row["Url"]
                    description = self.get_alibaba_description_and_images(url)

                    # Guardar en un archivo .txt
                    txt_file_name = f"producto_{index}.txt"  # Puedes cambiarlo para que sea más descriptivo
                    save_description_to_txt(description, self.data_path=='img', txt_file_name)
    
    def get_alibaba_description_and_images(self, url):
        # Configurar Selenium con Chrome
        options = Options()
        options.add_argument("--headless")  # Para ejecutar en segundo plano
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        # Inicializar el navegador
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(5)  # Esperar a que cargue la página
        images_urls = []
        
        try:            
             # 1️⃣ Encontrar miniaturas de imágenes
            thumbnails = driver.find_elements(By.CSS_SELECTOR, "div.ProductImageThumbsList")
            # 2️⃣ Hacer clic en cada miniatura para cambiar la imagen principal
            for index, thumb in enumerate(thumbnails):
                try:
                    ActionChains(driver).move_to_element(thumb).click().perform()
                    time.sleep(2)  # Esperar cambio de imagen

                    # 3️⃣ Extraer la URL de la imagen principal
                    main_image = driver.find_element(By.CSS_SELECTOR, "img.id-h-full.id-w-full")
                    img_url = main_image.get_attribute("src")
                    
                    if img_url and img_url not in images_urls:
                        images_urls.append(img_url)
                        save_image(img_url, self.data_path, f"img_{index}")

                except Exception as e:
                    print(f"⚠️ No se pudo hacer clic en la miniatura {index}: {e}")

            
            # Intentar encontrar la descripción en el div con id="J-rich-text-description"
            try:
                description_element = driver.find_element(By.ID, "J-rich-text-description")
                description_text = description_element.text.strip()
            except:
                description_text = "Descripción no encontrada"
            
            return description_text
            
        finally:
            driver.quit()

if __name__ == '__main__':
    # URL de prueba
    url = "https://spanish.alibaba.com/product-detail/2112-Commercial-Industrial-Poultry-Quail-Reptile-1600227849205.html"
    descripcion = Scraper_description('data')
    descripcion_texto = descripcion.get_alibaba_description_and_images(url)
    print(f"Descripción:\n{descripcion_texto}")
    