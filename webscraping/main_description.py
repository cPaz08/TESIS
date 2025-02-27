import os
import pandas as pd
from scraper.scraper_description import Scraper_description
from config import *

if __name__ == '__main__':
    scraper_description = Scraper_description(DATA_PATH_ALIBABA)
    scraper_description.process_csv_files()
    