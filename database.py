from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.sql import select
import sqlalchemy
from google.cloud.sql.connector import Connector
import os
from dotenv import load_dotenv

import google.auth

# auth.authenticate_user()

# initialize Connector object
load_dotenv()
connector = Connector()
def getconn():
    conn = connector.connect(
        os.getenv('INSTANCE_CONNECTION_NAME'),
        "pymysql",
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        db=os.getenv('DB_NAME')
    )
    return conn

engine = create_engine(
    "mysql+pymysql://",
    creator=getconn,
)
# get a connection
# conn = pool.connect()

# connect to connection pool
# with pool.connect() as db_conn:
  # create coin_po table in our coins database
metadata_obj = MetaData()
po = Table(
    "coin_po",
    metadata_obj,
    Column("po", Integer, primary_key=True),
    Column("description", String(50)),
    Column("grade", Integer),
    Column("cost", Integer),
)

metadata_obj.create_all(engine)

conn = engine.connect()

ins = po.insert().values(description="coin desc", grade=65, cost=150)
result = conn.execute(ins)
#   db_conn.execute(
#     sqlalchemy.text(
#       "CREATE TABLE IF NOT EXISTS coin_po "
#       "( po integer NOT NULL, name VARCHAR(255) NOT NULL, "
#       "origin VARCHAR(255) NOT NULL, rating FLOAT NOT NULL, "
#       "PRIMARY KEY (po));"
#     )
#   )
#   # insert data into our ratings table
#   insert_stmt = sqlalchemy.text(
#       "INSERT INTO ratings (name, origin, rating) VALUES (:name, :origin, :rating)",
#   )

  # insert entries into table
#   db_conn.execute(insert_stmt, parameters={"name": "HOTDOG", "origin": "Germany", "rating": 7.5})
#   db_conn.execute(insert_stmt, parameters={"name": "BÀNH MÌ", "origin": "Vietnam", "rating": 9.1})
#   db_conn.execute(insert_stmt, parameters={"name": "CROQUE MADAME", "origin": "France", "rating": 8.3})

  # query and fetch ratings table
# results = conn.execute(sqlalchemy.text("SELECT * FROM coin_po")).fetchall()
s = select(po)
results = conn.execute(s)
  # show results
for row in results:
    print(row)