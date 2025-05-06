from src.preprocessing.functions import expresiones_regulares,tokenizar
import pandas as pd
from sqlalchemy import create_engine, text
from config.settings import DB_CONNECTION_STRING


# Leer el archivo SQL
with open("sql_queries\queries.sql", "r", encoding="utf-8") as file:
    query = file.read()

# Parámetros para la consulta
params = {
    "medico": "PSICOLOGÍA",
    "fechaini": "2023-01-01",
    "fechafin": "2025-05-04"
}

# Crear conexión y ejecutarS
engine = create_engine(DB_CONNECTION_STRING)
with engine.connect() as conn:
    historias_clinicas = pd.read_sql(text(query), conn, params=params)
    
#Procesamiento de columna Subejetivo
#preprocessed_data = historias_clinicas["SUBJETIVO"].head(10)
processed_data = expresiones_regulares(historias_clinicas["SUBJETIVO"].head(100))
daots_tokenizados = tokenizar(processed_data.head(100))
daots_tokenizados.to_excel("datos_tokenizados.xlsx", index=False)

#Procesamiento de coluna Objetivo 
processed_data_objetivo = expresiones_regulares(historias_clinicas["OBJETIVO"].head(100))
daots_tokenizados_objetivo = tokenizar(processed_data_objetivo.head(100))
daots_tokenizados_objetivo.to_excel("datos_tokenizados_objetivo.xlsx", index=False) 
