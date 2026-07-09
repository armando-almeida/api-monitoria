from pymongo import MongoClient
import pandas as pd

#substitua "mongodb://localhost:27017" pela string de conexão do seu banco de dados MongoDB
client = MongoClient("mongodb://localhost:27017")

db = client["monitoria"]

colecao = db["dados_monitoria"]

df = pd.read_csv("dados_com_semestre.csv")

dados = df.to_dict(orient="records")

colecao.insert_many(dados)

print(f"{len(dados)} registros inseridos.")