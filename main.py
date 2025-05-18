from src.preprocessing.functions import expresiones_regulares,tokenizar,lematizar,label_encodering
import pandas as pd
from sqlalchemy import create_engine, text
from config.settings import DB_CONNECTION_STRING
import time
from sklearn.feature_extraction.text import TfidfVectorizer
import string


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

#n para head
n=5000
    
#Procesamiento de columna Subejetivo
preprocessed_data = historias_clinicas["Concatenada"].head(n)
start_time=time.time()
processed_data = expresiones_regulares(historias_clinicas["Concatenada"].head(n))
datos_tokenizados = tokenizar(processed_data.head(n))
datos_lemantizados = lematizar(datos_tokenizados.head(n))
categorySexo=pd.DataFrame(label_encodering(historias_clinicas["SEXO"].head(n)),columns=["Sexos"])
categotyGrupo=pd.DataFrame(label_encodering(historias_clinicas["GRUPO"].head(n)),columns=["Grupos"])
datos_lemantizados=pd.concat([categorySexo,categotyGrupo,datos_lemantizados],axis=1)
datos_lemantizados.to_excel("datos_lemantizados.xlsx", index=False)
datos_tokenizados.to_excel("datos_tokenizados.xlsx", index=False)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tiempo de ejecución: {elapsed_time:.2f} segundos")



# Guardar DataFrame procesado como archivo parquet
historias_clinicas.to_parquet("data/processed/historias_clinicas.parquet", index=False)
historias_clinicas.to_excel("historias_clinicas.xlsx", index=False)


print(historias_clinicas.head(n))

datos_lemantizados["Concatenado1"]=datos_lemantizados["Concatenada"].apply(lambda x: " ".join(x))

vectorizer=TfidfVectorizer()
x_vect= vectorizer.fit_transform(datos_lemantizados["Concatenado1"])
df_vect=pd.DataFrame(x_vect.toarray(),columns=vectorizer.get_feature_names_out())

df_final=pd.concat([datos_lemantizados.drop(columns=["Concatenada","Concatenado1"]).reset_index(drop=True),df_vect.reset_index(drop=True)],axis=1)
df_final.to_parquet("datos_vectorizados.parquet", index=False)