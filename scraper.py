import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import os

def scrape():
    url = "https://csg.com.br"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    lines = soup.get_text(separator="\n").splitlines()
    clean_lines = [l.strip() for l in lines if l.strip()]

    rodovia = None
    impacto = None
    data_coleta = date.today().isoformat()

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

    df = pd.DataFrame(avisos)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/avisos.csv", index=False)
    print("Atualizado com sucesso!")


if __name__ == "__main__":
    scrape()