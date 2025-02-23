from scraper.scraper import scrape
from config import *

if __name__ == "__main__":
    scrape(URL_BASE_MERCADO_LIBRE, OUTPUT_MERCADO_LIBRE_DATA)