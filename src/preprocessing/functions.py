import re 
import pandas as pd
import spacy
from spacy.lang.es.stop_words import STOP_WORDS as stopwords



def expresiones_regulares(columna):
    # Asegura que la columna sea texto
    columna = columna.astype(str).str.lower()

    # Aplica la limpieza fila por fila
    return columna.apply(lambda x: re.sub(r'\s+', ' ', re.sub(r'[^a-zñü ]', '', x)).strip())


import spacy
import pandas as pd

def tokenizar(columna: pd.Series) -> pd.Series:
    # Cargar modelo solo una vez (más eficiente si llamas varias veces la función)
    nlp = spacy.load("es_core_news_sm")
    stopwords = nlp.Defaults.stop_words

    # Asegurarse de que todos los valores sean string y reemplazar nulos
    columna = columna.astype(str).fillna("")

    # Aplicar tokenización con manejo de errores
    columna_tokenizada = columna.apply(
        lambda x: [
            token.text for token in nlp(x)
            if token.text not in stopwords and not token.is_punct and not token.is_space
        ]
    )
    return columna_tokenizada
