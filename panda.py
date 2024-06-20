import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("games.csv")

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/games")

df_100 = df.head(100)
df_100.to_sql("games", engine, if_exists="replace", index=False)

print("Datos guardados en la base de datos con éxito")
