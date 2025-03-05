# scraper/utils.py
import csv
import pandas as pd
import os
from pathlib import Path
import requests
import re

def sanitize_filename(filename, max_length=100):
    """
    Sanitiza el nombre del archivo para evitar caracteres inválidos y limitar su longitud.
    """
    if not isinstance(filename, str):  # Asegurar que es string
        filename = "sin_nombre"

    # Reemplazar caracteres no permitidos
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)  
    # Reemplazar espacios en blanco con guiones bajos
    filename = re.sub(r'\s+', "_", filename)

    # Eliminar espacios al inicio y final
    filename = filename.strip()
    return filename[:max_length]  # Limitar la longitud máxima

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

    # Validar los parámetros de entrada
    if not data_path or not isinstance(data_path, str):
        raise ValueError("❌ El parámetro 'data_path' es inválido o vacío.")
    if not file_name or not isinstance(file_name, str):
        raise ValueError("❌ El parámetro 'file_name' es inválido o vacío.")

    # Construir la ruta de la carpeta
    descriptions_dir = os.path.join(data_path.replace('/processed/alibaba', ''), "descriptions")
    txt_file_dir = os.path.join(descriptions_dir, file_name.replace('.txt', ''))
    os.makedirs(txt_file_dir, exist_ok=True)  # Crear 'descriptions' de cada txt si no existe

    txt_file_path = os.path.join(txt_file_dir, file_name)

    try:
        # Guardar la descripción en un archivo .txt
        with open(txt_file_path, "w", encoding="utf-8") as file:
            file.write(description)
        print(f"✅ Descripción guardada en: {txt_file_path}")
        return txt_file_dir
    except Exception as e:
        print(f"❌ Error al guardar la descripción: {e}")

def download_img(image_urls, output_folder):
    # Filtro
    filtro = ['720x720']
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, img_url in enumerate(image_urls):
        if not any(word in img_url for word in filtro):
            continue
        try:
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                image_path = os.path.join(output_folder, f"imagen_{i+1}.jpg")
                with open(image_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"✅ Imagen {i+1} descargada: {image_path}")
            else:
                print(f"❌ No se pudo descargar la imagen {i+1}")
        except Exception as e:
            print(f"❌ Error al descargar la imagen {i+1}: {e}")
