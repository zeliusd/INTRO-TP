import os
import pandas
from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432/games_db")
try:
    with engine.connect() as connection:
        connection.execute(text("DROP TABLE games_tb CASCADE;"))
        connection.commit()
except Exception as e:
    print(e)
    pass

os.system("unzip db/games_data.zip")
df = pandas.read_csv("games.csv")

df.columns = df.columns.str.replace(" ", "_").str.lower()

df_100 = df.head(100)

df_100.to_sql("games_tb", engine, if_exists="replace", index=False)

with engine.connect() as connection:
    connection.execute(text("ALTER TABLE games_tb ADD PRIMARY KEY (appid);"))
    connection.commit()

os.system("rm games.csv")
