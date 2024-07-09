import os
import pandas
from sqlalchemy import create_engine

os.system("unzip db/games_data.zip")
data_frame = pandas.read_csv("games.csv")

engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432/games_db")

data_frame.columns = data_frame.columns.str.replace(" ", "_").str.lower()

# df_100 = df.head(100)

data_frame.to_sql("games_tb", engine, if_exists="replace", index=False)

print("Datos guardados en la base de datos con éxito")

os.system("rm games.csv")
