# update_data.py
import pandas as pd
from scraper import scrape_csg

def append_csv():
    new = scrape_csg()
    try:
        df = pd.read_csv("data/avisos.csv")
        df = pd.concat([df, new], ignore_index=True)
    except FileNotFoundError:
        df = new
    df.drop_duplicates(subset=["data","aviso"], inplace=True)
    df.to_csv("data/avisos.csv", index=False)
