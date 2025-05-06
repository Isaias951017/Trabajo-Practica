import re 
import pandas as pd
import spacy
from spacy.lang.es.stop_words import STOP_WORDS as stopwords



def expresiones_regulares(columna):
    # Asegura que la columna sea texto
    columna = columna.astype(str).str.lower()

    # Aplica la limpieza fila por fila
    return columna.apply(lambda x: re.sub(r'\s+', ' ', re.sub(r'[^a-zñü ]', '', x)).strip())


def tokenizar(columna: pd.Series) -> pd.Series:
    nlp = spacy.load("es_core_news_sm")
    
    columna_tokenizada = columna.apply(lambda x: [token.text for token in nlp(x) if token.text not in stopwords])
    return columna_tokenizada