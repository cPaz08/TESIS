import os
import pandas as pd
from scraper.scraper_description import Scraper_description
from config import *

if __name__ == '__main__':
    scraper_description = Scraper_description(DATA_PATH_ALIBABA)
    try:
        scraper_description.process_csv_url()
    except KeyboardInterrupt:
        print("🚨 Extracción interrumpida manualmente.")
    finally:
        scraper_description.close_driver()
    