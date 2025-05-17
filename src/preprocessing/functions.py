import re 
import pandas as pd
import spacy
from spacy.lang.es.stop_words import STOP_WORDS as stopwords
from sklearn import preprocessing



def expresiones_regulares(columna):
    
    columna = columna.astype(str).str.lower()

    # Aplica la limpieza fila por fila
    return columna.apply(lambda x: re.sub(r'\s+', ' ', re.sub(r'[^a-zñü ]', '', x)).strip())



def tokenizar(columna: pd.Series) -> pd.Series:
    
    nlp = spacy.load("es_core_news_sm")
    stopwords = nlp.Defaults.stop_words
    stopwords_personalizados = ["medico", "paciente", "psicologo", "psicologa", "psicologia", "psicoterapeuta", "psicoterapia","paciente","refiere"]
    stopwords.update(stopwords_personalizados)
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

def lematizar(columna: pd.Series) -> pd.Series:
    nlp = spacy.load("es_core_news_sm")
    tokens = columna.apply(lambda x: [token for token in nlp(" ".join(x))])
    lemas = tokens.apply(lambda x: [token.lemma_ for token in x])   
    return lemas


def label_encodering(columna: pd.Series) -> pd.Series:
    label_encoder=preprocessing.LabelEncoder()
    columna=label_encoder.fit_transform(columna)
    return columna
    