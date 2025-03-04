# scraper/utils.py
import csv
import pandas as pd
import os
from pathlib import Path
import requests

def save_to_csv(data, filename):
    '''Crea un archivo CSV desde 0 y guarda los datos usando pandas.'''
    if not data:
        print('🚫 No hay datos para guardar.')
        return
    
    # Crear carpeta si no existe
    folder = os.path.dirname(filename)  # Extrae la carpeta del filename
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    
    df = pd.DataFrame(data)  # Convierte la lista de diccionarios en un DataFrame
    df.to_csv(filename, index=False, encoding='utf-8')  # Guarda sin índice

    print(f'✅ Datos guardados en {filename}')

def save_description_to_csv(df, DATA_PATH, file_name):
    folder_path = Path(DATA_PATH) / "description"
    folder_path.mkdir(parents=True, exist_ok=True)  # Crea la carpeta si no existe

    new_file_path = folder_path / file_name.replace(".csv", "_descriptions.csv")

    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")
    print(f"✅ Archivo guardado: {new_file_path.resolve()}")  # Ruta absoluta


def save_description_to_txt(description, data_path, file_name):
    """
    Guarda la descripción en un archivo .txt en la carpeta 'descriptions'.
    """
    folder_path = os.path.join(data_path, "descriptions")  # Carpeta donde guardamos los TXT
    os.makedirs(folder_path, exist_ok=True)  # Crear la carpeta si no existe

    txt_file_path = os.path.join(folder_path, file_name.replace(".csv", ".txt"))  # Nombre del archivo TXT

    with open(txt_file_path, "w", encoding="utf-8") as file:
        file.write(description)

    print(f"✅ Descripción guardada en: {txt_file_path}")

def save_image(img_url, folder_path, image_name):
    """ Descarga y guarda una imagen desde una URL """
    if not img_url:
        return None

    response = requests.get(img_url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(folder_path, f"{image_name}.jpg")
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"✅ Imagen guardada: {file_path}")
        return file_path
    return None
