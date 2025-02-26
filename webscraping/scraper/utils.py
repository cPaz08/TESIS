# scraper/utils.py
import csv
import pandas as pd
import os

def save_to_csv(data, filename):
    '''Crea un archivo CSV desde 0 y guarda los datos usando pandas.'''
    if not data:
        print('No hay datos para guardar.')
        return
    
    # Crear carpeta si no existe
    folder = os.path.dirname(filename)  # Extrae la carpeta del filename
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    
    df = pd.DataFrame(data)  # Convierte la lista de diccionarios en un DataFrame
    df.to_csv(filename, index=False, encoding='utf-8')  # Guarda sin índice

    print(f'Datos guardados en {filename}')

def process_csv_files(DATA_PATH):
    for file in os.listdir(DATA_PATH):
        if file.endswith(".csv"):
            file_path = os.path.join(DATA_PATH, file)
            print(f"📂 Procesando {file_path}...")

            df = pd.read_csv(file_path)

            if "url" in df.columns:
                df["description"] = df["url"].apply(get_product_description)

                new_file_path = file_path.replace(".csv", "_descriptions.csv")
                df.to_csv(new_file_path, index=False, encoding="utf-8-sig")
                print(f"✅ Archivo guardado: {new_file_path}")
            else:
                print(f"⚠️ El archivo {file} no tiene una columna 'url'.")

if __name__ == "__main__":
    process_csv_files()
