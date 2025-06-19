import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import pytz

def scrape():
    url = "https://csg.com.br"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    lines = soup.get_text(separator="\n").splitlines()
    clean_lines = [l.strip() for l in lines if l.strip()]

    rodovia = None
    impacto = None
    
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    data_coleta = datetime.now(brasilia_tz).date().isoformat()

    avisos = []

    for linha in clean_lines:
        if any(linha.startswith(p) for p in ["ERS-", "RSC-", "BRS-"]):
            rodovia = linha
        elif "IMPACTO" in linha.upper():
            impacto = linha
        elif linha.startswith("*") and rodovia and impacto:
            avisos.append({
                "data_coleta": data_coleta,
                "rodovia": rodovia,
                "impacto": impacto,
                "aviso": linha
            })


    df_novo = pd.DataFrame(avisos)

    os.makedirs("data", exist_ok=True)
    path_csv = "data/avisos.csv"

    if os.path.exists(path_csv):
        df_antigo = pd.read_csv(path_csv)
        df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
        df_final.drop_duplicates(subset=["data_coleta", "rodovia", "impacto", "aviso"], inplace=True)
    else:
        df_final = df_novo

    df_final.to_csv(path_csv, index=False)
    print("Atualizado com sucesso!")


if __name__ == "__main__":
    scrape()