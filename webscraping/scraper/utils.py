# scraper/utils.py
import csv

def save_to_csv(data, filename):
    '''Guarda los datos en un archcivo CSV.'''
    if not data:
        print('No hay datos para guardar.')
        return
    
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

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