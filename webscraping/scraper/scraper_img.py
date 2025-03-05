from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os

# Configurar Selenium con ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Opcional, para ejecutar en segundo plano
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL de la página de Alibaba
url = "https://spanish.alibaba.com/product-detail/2112-Commercial-Industrial-Poultry-Quail-Reptile-1600227849205.html"  # Reemplaza con la URL específica del producto

# Abrir la página
driver.get(url)
time.sleep(5)  # Esperar a que cargue la página

# Encontrar imágenes en la página
imagenes = driver.find_elements(By.TAG_NAME, "img")

# Extraer y mostrar las URLs de las imágenes
image_urls = [img.get_attribute("src") for img in imagenes if img.get_attribute("src")]

# Filtro
filtro = ['720x720']
# Carpeta donde se guardarán las imágenes
output_folder = "imagenes_alibaba"
os.makedirs(output_folder, exist_ok=True)

# Imprimir las URLs de las imágenes
for i, img_url in enumerate(image_urls):
    if not any(word in img_url for word in filtro):
        continue
    print(f"Imagen {i+1}: {img_url}")
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            image_path = os.path.join(output_folder, f"imagen_{i+1}.jpg")
            with open(image_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Imagen {i+1} descargada: {image_path}")
        else:
            print(f"No se pudo descargar la imagen {i+1}")
    except Exception as e:
        print(f"Error al descargar la imagen {i+1}: {e}")

# Cerrar Selenium
driver.quit()

