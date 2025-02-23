# scraper/utils.py
import csv
import pandas as pd

def save_to_csv(data, filename):
    '''Crea un archivo CSV desde 0 y guarda los datos usando pandas.'''
    if not data:
        print('No hay datos para guardar.')
        return
    
    df = pd.DataFrame(data)  # Convierte la lista de diccionarios en un DataFrame
    df.to_csv(filename, index=False, encoding='utf-8')  # Guarda sin índice

    print(f'Datos guardados en {filename}')


def save_txt(data, filename):
    '''Guarda los datos en un archcivo txt.'''
    if not data:
        print('No hay datos para guardar.')
        return
    
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

        print(f'Datos guardados en {filename}')