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

# Crear conexión y ejecutar
engine = create_engine(DB_CONNECTION_STRING)
with engine.connect() as conn:
    historias_clinicas = pd.read_sql(text(query), conn, params=params)
    

preprocessed_data = historias_clinicas["SUBJETIVO"].head(10)

preprocessed_data.to_excel("preprocessed_data.xlsx", index=False)

processed_data = expresiones_regulares(historias_clinicas["SUBJETIVO"]).head(10)

processed_data.to_excel("processed_data.xlsx", index=False)

