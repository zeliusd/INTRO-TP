import os
import pandas
from sqlalchemy import create_engine

os.system("unzip db/games_data.zip")
df = pandas.read_csv("games.csv")

engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432/games_db")

df.columns = df.columns.str.replace(" ", "_").str.lower()

df_100 = df.head(100)

df_100.to_sql("games_tb", engine, if_exists="replace", index=False)

print("Datos guardados en la base de datos con éxito")

os.system("rm games.csv")
